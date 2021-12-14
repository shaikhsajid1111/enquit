from django.http import JsonResponse
from users.models import CustomUser
from post.models import Post, Vote, Report, Images, Answer_Vote, Answer, Vault
from django.contrib.auth.decorators import login_required
import cloudinary  # external library
import cloudinary.uploader  # external library
from django.contrib import messages
from django.shortcuts import redirect


def fetch_posts(request, page_number):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
            user_data = CustomUser.objects.get(
                user=request.user)  # fetch the user from database
            offset = (int(page_number)*10)-10
            limits = int(page_number)*10
            posts = Post.objects.all()[offset:limits]
            posts_data = []
            for post in posts:
                data = {}

                already_voted = Vote.objects.filter(
                    user=user_data, post=post) and True or False
                try:
                    votes = Vote.objects.filter(post=post).count()
                except Vote.DoesNotExist:
                    votes = 0
                data['votes'] = votes

                try:
                    images = Images.objects.filter(post=post)
                except Images.DoesNotExist:
                    images = []

                data['images'] = images
                data['post'] = post
                data['already_voted'] = already_voted
                posts_data.append(data)
            # send the data to home page as well
            return JsonResponse({"user_data": user_data, "posts_data": (posts_data)})
        else:
            # if the user is unauthenticated
            messages.warning(request, "Only Registered user allowed")
            return redirect("/account/signup")
    except Exception as ex:
        return redirect("/account/signup")


@login_required
def vote_post(request, post_id):
    if request.method == "POST":
        user = CustomUser.objects.get(user=request.user)
        post = Post.objects.get(post_id=post_id)
        new_vote, created = Vote.objects.get_or_create(user=user, post=post)
        return JsonResponse({"Liked": True})


@login_required
def vote_answer(request, answer_id):
    if request.method == "POST":
        user = CustomUser.objects.get(user=request.user)
        answer = Answer.objects.get(id=answer_id)
        new_vote, created = Answer_Vote.objects.get_or_create(
            user=user, answer=answer)
        return JsonResponse({"Liked": True})


@login_required
def report_post(request, post_id):
    if request.method == "POST":
        user = CustomUser.objects.get(user=request.user)
        post = Post.objects.get(post_id=post_id)
        new_report, created = Report.objects.get_or_create(
            user=user, post=post)
        report_counts = Report.objects.filter(post=post).count()
        number_of_users = CustomUser.objects.all().count()
        print("Percentage: ", (2/100)*number_of_users)
        if report_counts > (2/100)*number_of_users:
            images = Images.objects.filter(post=post)
            for image in images:
                cloudinary.uploader.destroy(image.public_id)
            post.delete()
        return JsonResponse({"Reported": True})


@login_required
def save_answer(request, post_id):
    if request.method == "POST":
        user = CustomUser.objects.get(user=request.user)
        post = Post.objects.get(post_id=post_id)
        item = Vault.objects.create(user=user, post=post)
        item.save()
        return JsonResponse({"Saved": True})
