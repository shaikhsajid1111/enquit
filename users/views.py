from django.shortcuts import render,redirect
from users.models import CustomUser
from .utils import get_image,password_is_valid
from django.contrib import messages
from django.contrib.auth.models import User
from random_username.generate import generate_username
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required


def login_user(request):
  if request.method == "GET": #check if the request we got is HTTP GET request
    if request.user.is_authenticated and not request.user.is_superuser: #check if the user is already authenticated user
      #if the user is authenticated, the redirect them to home page again
      return redirect("/home")
    #if the user is unauthenticated then redirect to login page
    return render(request,"login.html") #rendering the login.html
  if request.method == "POST":  #check if the request we got is HTTP POST request
    username = request.POST['username'] #fetch the username from the submitted form
    password = request.POST['password'] #fetch the password from the submitted form
    user = authenticate(username=username,password=password) #authenticate if the credentials are valid
    if user is not None: #if user matched the given credentials
      login(request,user) #login the user
      return redirect("/home") #send them to home page
    else:
      #if no user with such credentials was found
      messages.error(request,"Invalid Credentials!") #set the error message
      return redirect("/auth/login") #redirect user back to login page again

@login_required
def log_out(request):
  if request.user.is_authenticated:
    #if the user is authenticated
    logout(request) #log out the user
    return redirect("/auth/login") #redirect them back to login page

@login_required
def delete_user(request):
  if request.method == "GET": #if the request for account delection is GET method, redirect them to delete page only
    return render(request,"delete_user.html")
  if request.method == "POST": #if the form have been submitted with POST request
    username = request.POST['username'] #fetch the username from the submitted form
    password = request.POST['password'] #fetch the password from the submitted form
    # authenticate if the credentials are valid
    user = authenticate(username=username, password=password)
    if user is not None:
      #if user matched the given credentials
      logout(request) #log out first and clear the sessions
      user.delete() #delete the user from the database
      messages.info(request,"Its sad to let you go :(") #just a message to express sad that user is leaving the site
      return redirect("/auth/login") #redirect them back to login
    else:
      messages.error(request,"Invalid credentials!, Can't delete the account") #if the credentials are incorrect
      return redirect("/auth/delete") #send them back to the same page


def signUp(request):
  if request.method == "GET":  # if the request for account creation is GET method, redirect them to signup page.
    if request.user.is_authenticated and not request.user.is_superuser:
      #if the user is authnticated and is not the admin
      return redirect("/home") #send them to home
    return render(request,"signup.html") #if any conditiona dissatisfies, then send to signup form
  elif request.method == "POST": #if the form have been submitted
    email = request.POST['email'] #fetch the email from the form request
    password = request.POST['password'] #fetch the password from the form request
    confirm_password = request.POST['confirm_password'] #fetch the password again from the form request, to verify that password are same
    gender = request.POST['gender'] #fetch the gender from the form request
    age = request.POST['age']  # fetch the age from the form request
    if password == confirm_password: #if both the passwords are same
      if password_is_valid(password): #if password meets the password criteria
        try:
          user = User.objects.get(email=email) #search for email, if it already exists in database
          if user:
            #if the user is found that means, the email have been used already and cannot be re-used
            messages.error(request,"Email already exists!") #set the error message
            return render(request,"signup.html") #rediret back to signup page

        except User.DoesNotExist: #if the user does not exists, it means its a new email, start the registration process
          username = generate_username(1)[0] #generate a random username
          image = get_image(gender=gender,age=age) #get the random image generated with AI using API call
          user = User.objects.create_user(username=username,password=password,email=email) #create the user object
          custom_user = CustomUser(user=user, profile_picture_link=image) #now create the exended model object and set one-to-one relationship with the User object
          custom_user.save() #save the user
          login(request,user) #login the new user
          return redirect("/home") #send them to home page
    else:
      #if the passwords do not match
      messages.warning(request,"Passwords do not match")
      return render(request,"signup.html") #send them back to signup page

