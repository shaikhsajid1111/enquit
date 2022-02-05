from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from django.shortcuts import render, redirect
from django.contrib import messages
from post.models import Post, Vote, Tags, Medias, Vault
from django.db.models import Q


@login_required
def blank_route(request):
    return redirect("/home/1")


@login_required
def home(request, page_number):
    """this views is called when the user hits the route domain/home"""
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
            user_data = CustomUser.objects.get(
                user=request.user)  # fetch the user from database
            offset = (int(page_number)*10)-10  # number of entry to leave
            limits = int(page_number)*10  # number of entry limit
            posts = Post.objects.all()[offset:limits]
            last_entry = Post.objects.last()
            try:
              is_last_page = True if last_entry == (list(posts))[-1] else False
            except IndexError:
              is_last_page = True
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
                    medias = Medias.objects.filter(post=post)
                except Medias.DoesNotExist:
                    medias = []
                try:
                    tags = Tags.objects.filter(tag=post)
                    tags = [tag.text for tag in tags]
                except Tags.DoesNotExist:
                    tags = []
                try:
                  is_saved = Vault.objects.get(
                        post=post, user=user_data)
                  is_saved = True
                except Vault.DoesNotExist:
                  is_saved = False
                data['medias'] = medias
                data['post'] = post
                data['already_voted'] = already_voted
                data['tags'] = tags
                data['is_saved'] = is_saved
                posts_data.append(data)
            # send the data to home page as well
            return render(request, "home.html", {"user_data": user_data, "posts_data": (posts_data), "title": "Website Name", "next_page": int(page_number)+1, "is_last_page": is_last_page})
        else:
            # if the user is unauthenticated
            messages.warning(request, "Only Registered user allowed")
            return redirect("/account/signup")
    except Exception as ex:
        print("Home Route: ", ex)
        return redirect("/account/signup")


def search(request, page_number):
    if request.method == "GET":
        query = request.GET['query']
        offset = (int(page_number)*10)-10  # number of entry to leave
        limits = int(page_number)*10  # number of entry limit
        # if query is not empty
        if query != "":
            if query.startswith("@"):
                # if query starts with @ then it means we need to find user
                users_data = CustomUser.objects.filter(
                    user__username__contains=str(query).removeprefix("@"))[offset:limits]
                last_entry = CustomUser.objects.last()
                try:
                  is_last_page = True if last_entry == (
                    list(users_data))[-1] else False
                except IndexError:
                  is_last_page = True
                return render(request, "search.html", {"users_data": users_data,
                                                       "type": "user", "title": "Results for {}".format(query),
                                                       "next_page": int(page_number)+1, "query": query, "is_last_page": is_last_page})
            elif query.startswith("#"):
                user_data = CustomUser.objects.get(
                    user=request.user)  # fetch the user from database
                posts_tags = Tags.objects.filter(
                    text=str(query).removeprefix("#"))[offset:limits]
                posts = [post.tag for post in posts_tags]
                last_entry = Tags.objects.filter(
                    text=str(query).removeprefix("#")).last()
                try:
                  is_last_page = True if last_entry.tag == posts[-1] else False
                except IndexError:
                  is_last_page = False
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
                      is_saved = Vault.objects.get(
                        post=post, user=user_data)
                      is_saved = True
                    except Vault.DoesNotExist:
                      is_saved = False
                    try:
                        medias = Medias.objects.filter(post=post)
                    except Medias.DoesNotExist:
                        medias = []
                    try:
                        tags = Tags.objects.filter(tag=post)
                        tags = [tag.text for tag in tags]
                    except Tags.DoesNotExist:
                        tags = []
                    data['medias'] = medias
                    data['post'] = post
                    data['already_voted'] = already_voted
                    data['tags'] = tags
                    data['is_saved'] = is_saved
                    posts_data.append(data)
                return render(request, "search.html", {"posts_data": posts_data,
                                                       "type": "tags", "title": "Results - {}".format(query),
                                                       "next_page": int(page_number)+1, "query": query, "is_last_page": is_last_page})
            else:
                # if the query starts with text then it means we need to find from the text
                user_data = CustomUser.objects.get(
                    user=request.user)  # fetch the user from database
                posts = Post.objects.filter(
                    Q(text__contains=str(query)) | Q(title__contains=str(query)))[offset:limits]
                last_entry = Post.objects.filter(
                    Q(text__contains=str(query)) | Q(title__contains=str(query))).last()
                try:
                  is_last_page = True if last_entry == (
                    list(posts))[-1] else False
                except IndexError:
                  is_last_page = True
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
                        medias = Medias.objects.filter(post=post)
                    except Medias.DoesNotExist:
                        medias = []
                    try:
                        tags = Tags.objects.filter(tag=post)
                        tags = [tag.text for tag in tags]
                    except Tags.DoesNotExist:
                        tags = []
                    try:
                      is_saved = Vault.objects.get(
                        post=post, user=user_data)
                      is_saved = True
                    except Vault.DoesNotExist:
                      is_saved = False
                    data['medias'] = medias
                    data['post'] = post
                    data['already_voted'] = already_voted
                    data['tags'] = tags
                    data['is_saved'] = is_saved
                    posts_data.append(data)
                return render(request, "search.html", {"posts_data": posts_data, "type": "post",
                                                       "title": "Results for {}".format(query), "next_page": int(page_number)+1,
                                                       "query": query, "is_last_page": is_last_page})
        else:
            return redirect("/")
