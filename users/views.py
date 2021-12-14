from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from users.models import CustomUser
from .utils import get_image, password_is_valid
from django.contrib import messages
from django.contrib.auth.models import User
from random_username.generate import generate_username
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.utils.encoding import force_text
import environ  # external library
from post.models import Post, Images
import cloudinary.uploader
# To read environment variable
env = environ.Env()
environ.Env.read_env()


def login_user(request):
    if request.method == "GET":  # check if the request we got is HTTP GET request
        # check if the user is already authenticated user
        if request.user.is_authenticated and not request.user.is_superuser:
            # if the user is authenticated, the redirect them to home page again
            return redirect("/")
        # if the user is unauthenticated then redirect to login page
        return render(request, "login.html")  # rendering the login.html
    if request.method == "POST":  # check if the request we got is HTTP POST request
        # fetch the username from the submitted form
        username = request.POST['username']
        # fetch the password from the submitted form
        password = request.POST['password']
        # authenticate if the credentials are valid
        user = authenticate(username=username, password=password)
        if user is not None:  # if user matched the given credentials
            login(request, user)  # login the user
            return redirect("/")  # send them to home page
        else:
            # if no user with such credentials was found
            # set the error message
            messages.error(request, "Invalid Credentials!")
            # redirect user back to login page again
            return redirect("/account/login")


@login_required
def log_out(request):
    if request.user.is_authenticated:
        # if the user is authenticated
        logout(request)  # log out the user
        return redirect("/account/login")  # redirect them back to login page


@login_required
def delete_user(request):
    if request.method == "GET":  # if the request for account delection is GET method, redirect them to delete page only
        return render(request, "delete_user.html")
    if request.method == "POST":  # if the form have been submitted with POST request
        # fetch the username from the submitted form
        username = request.POST['username']
        # fetch the password from the submitted form
        password = request.POST['password']
        # authenticate if the credentials are valid
        user = authenticate(username=username, password=password)
        if user is not None:
            # if user matched the given credentials
            logout(request)  # log out first and clear the sessions
            custom_user = CustomUser.objects.get(user=user)
            users_posts = Post.objects.filter(author=custom_user)
            for post in users_posts:
                images = Images.objects.filter(post=post)
                for image in images:
                    cloudinary.uploader.destroy(image.public_id)
                post.delete()
            custom_user.delete()  # delete the user from the database
            user.delete()
            # just a message to express sad that user is leaving the site
            messages.info(request, "Its sad to let you go :(")
            return redirect("/account/login")  # redirect them back to login
        else:
            # if the credentials are incorrect
            messages.error(
                request, "Invalid credentials!, Can't delete the account")
            # send them back to the same page
            return redirect("/account/delete")


def signUp(request):
    # if the request for account creation is GET method, redirect them to signup page.
    if request.method == "GET":
        if request.user.is_authenticated and not request.user.is_superuser:
            # if the user is authnticated and is not the admin
            return redirect("/")  # send them to home
        # if any conditiona dissatisfies, then send to signup form
        return render(request, "signup.html")
    elif request.method == "POST":  # if the form have been submitted
        email = request.POST['email']  # fetch the email from the form request
        # fetch the password from the form request
        password = request.POST['password']
        # fetch the password again from the form request, to verify that password are same
        confirm_password = request.POST['confirm_password']
        # fetch the gender from the form request
        gender = request.POST['gender']
        age = request.POST['age']  # fetch the age from the form request
        if password == confirm_password:  # if both the passwords are same
            # if password meets the password criteria
            if password_is_valid(password):
                try:
                    # search for email, if it already exists in database
                    user = User.objects.get(email=email)
                    if user:
                        # if the user is found that means, the email have been used already and cannot be re-used
                        # set the error message
                        messages.error(request, "Email already exists!")
                        # rediret back to signup page
                        return render(request, "signup.html")

                except User.DoesNotExist:  # if the user does not exists, it means its a new email, start the registration process
                    # generate a random username
                    username = generate_username(1)[0]
                    # get the random image generated with AI using API call
                    image = get_image(gender=gender, age=age)
                    user = User.objects.create_user(
                        username=username, password=password, email=email)  # create the user object
                    # now create the exended model object and set one-to-one relationship with the User object
                    custom_user = CustomUser(
                        user=user, profile_picture_link=image, is_verified=False)
                    custom_user.save()  # save the user
                    # the email subject that will be sent to users for account activation
                    mail_subject = "Activate Your Account By Verifiying with us!"
                    # variable to fetch the current site detail
                    current_site = get_current_site(request)
                    # convert the HTML file into string that will be sent via Email
                    message = render_to_string("email_template.html", {
                        "user": user,  # denotes the current user
                        "domain": current_site.domain,  # denotes the current website's domain
                        # UID that needs to be checked
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": account_activation_token.make_token(user)
                    })
                    to_email = email  # the email receipent host
                    send_mail(mail_subject, message, env('EMAIL_HOST'), [
                              to_email])  # send the mail to the user
                    login(request, user)  # login the new user
                    return redirect("/")  # send them to home page
            else:
                messages.warning(
                    request, "Passwords Must be more then 5 characters!")
                # send them back to signup page
                return render(request, "signup.html", {"title": "Sign Up With Us"})
        else:
            # if the passwords do not match
            messages.warning(request, "Passwords do not match")
            # send them back to signup page
            return render(request, "signup.html", {"title": "Sign Up With Us"})


def activate(request, uid64, token):
    """
    This function intends to activate the account when the user clicks on activation
    link sent to them.
    """
    User = get_user_model()
    try:
        # convert the UID passed to text
        uid = force_text(urlsafe_base64_decode(uid64))
        # get the CustomUser who clicked the the link
        user = CustomUser.objects.get(user=request.user)
        # get the related user with the UID
        related_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        # if the user was not found
        user = None
    if user is not None and account_activation_token.check_token(related_user, token):
        if user.is_verified is True:
            return HttpResponse("You're Already Registered user. Yeeeeeah :D")
        user.is_verified = True
        user.save()
        return HttpResponse("Thank you for registration, Have a great time posting! :)")
    else:
        # on invalid link throw this error
        return HttpResponse("We Apologize but your activation Link is Invalid!")


def view_user(request, username):
    user = User.objects.get(username=username)
    custom_user = CustomUser.objects.get(user=user)
    posts = Post.objects.filter(author=custom_user)[:10]
    # send the data to home page as well
    return render(request, "home.html", {"user_data": custom_user, "posts_data": (posts), "title": "Feed - {}".format(username)})
