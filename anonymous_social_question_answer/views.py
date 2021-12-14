from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from django.shortcuts import render, redirect
from django.contrib import messages
from post.models import Images, Post, Vote


@login_required
def home(request):
    """this views is called when the user hits the route domain/home"""
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
            user_data = CustomUser.objects.get(
                user=request.user)  # fetch the user from database
            posts = Post.objects.all()[:10]
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
            return render(request, "home.html", {"user_data": user_data, "posts_data": (posts_data), "title": "Website Name"})
        else:
            # if the user is unauthenticated
            messages.warning(request, "Only Registered user allowed")
            return redirect("/account/signup")
    except Exception as ex:
        print("Home Route: ", ex)
        return redirect("/account/signup")


def search(request):
    if request.method == "GET":
        query = request.GET['query']
        if query != "":
            if query.startswith("@"):
                return render(request, "search.html", {"data": CustomUser.objects.filter(user__username__contains=str(query).removeprefix("@")), "type": "user", "title": "Results for {}".format(query)})
            else:
                return render(request, "search.html", {"data": Post.objects.filter(text__contains=str(query)), "type": "post", "title": "Results for {}".format(query)})
        else:
            return redirect("/home")
