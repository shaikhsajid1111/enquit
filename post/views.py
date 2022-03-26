from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from isort import file
from users.models import CustomUser
from .models import Post, Medias, Answer, Vault, Tags, Vote
import cloudinary  # external library
import cloudinary.uploader  # external library
from django.http import HttpResponseRedirect
import mimetypes

@login_required(login_url="/account/login")
def create_post(request):
    """function to create post"""
    if request.method == "GET":
        try:
          user = CustomUser.objects.get(user=request.user, is_verified=True)
        #if GET request then render its HTML
          return render(request, "create_post.html",{"title":"Create a Post"})
        except CustomUser.DoesNotExist:
          messages.error(request, "Not Verified!")
          return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    if request.method == "POST":
        # extract respective content from the request
        user = CustomUser.objects.get(user=request.user,is_verified=True)
        if not user:
          messages.error(request, "Not Verified!")
          return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        text = request.POST['text']
        medias = request.FILES.getlist('medias')
        tags = request.POST['tags']
        title = request.POST['title']
        if title == "" or tags == "":
            messages.error(request, "Please fill entire details!")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        post = Post(text=text, author=user, title=title)  # create post
        post.save()
        for media in medias:
            # upload media to the cloudinary server
            if post is not None:
                filename = media.name
                filetype = mimetypes.guess_type(filename)
                if 'video' in filetype[0] or 'image' in filetype[0]:
                  result = cloudinary.uploader.upload_large(media)  # upload
                  # create object for the uploaded file
                  if 'video' in filetype[0]:
                    media_obj = Medias.objects.create(
                      url=result["url"], public_id=result['public_id'], post=post,media_type="video")
                  elif "image" in filetype[0]:
                    media_obj = Medias.objects.create(
                      url=result["url"], public_id=result['public_id'], post=post,media_type="image")
            else:
              messages.error(request, "Invalid Media Type!")
              return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        post.save()  # save to the DB
        for tag in tags.split(" "):
            # split out tags from the given tags
            tag_obj = Tags.objects.create(
                text=tag.lower(), tag=post)  # create tag obj
            tag_obj.save()  # save

        # send success message to the front-end
        messages.success(request, "Post Created Successfully!")
        return redirect("/")


@login_required(login_url="/account/login")
def delete_post(request, id):
    """function to delete post"""
    if request.method == "GET":
        try:
            # try to find the post
            post = Post.objects.get(post_id=id)
        except Post.DoesNotExist:
            # if post does not exists, set it to None
            post = None
        if post is None:
            # if post was not found
            # send error to front-end
            messages.error(request, "Post Does Not Exists!")
            return redirect("/")  # redirect to the homepage
        elif request.user.id != post.author.user.id:
            # if someone is trying to delete someone else's post
            # send error message to front-end
            messages.error(request, "Permission Denied!")
            return redirect("/")
        else:
            # if no problem occured, delete the post
            medias = Medias.objects.filter(post=post)
            for media in medias:
                # delete all the media of the post
                cloudinary.uploader.destroy(media.public_id)
            post.delete()  # delete the post
            messages.success(request, "Post deleted!")
            # to the home page
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="/account/login")
def view_post(request, post_id):
    """function to view post"""
    if request.method == "GET":
        post = Post.objects.get(post_id=post_id)  # find the post

        # find all parent answers, exclude the replies for the answer hence the "parent=None" was passed
        answers = Answer.objects.filter(post=post, parent=None)
        medias = Medias.objects.filter(post=post)
        data = []
        for answer in answers:
            # traverse through all answers and find their replies as well
            temp_data = {}
            temp_data['answer'] = answer
            replies_list = []
            try:
                # find all replies to the parent answer
                replies = Answer.objects.filter(parent=answer)
            except:
                # if error occurs in finding
                replies = []
            for reply in replies:
                # traverse over the replies and save it to the list
                replies_list.append(reply)
            temp_data['replies'] = replies_list
            data.append(temp_data)  # append the dict into the list
        return render(request, "post_details.html", {"post_data": post,
                                                     "answers": data, "medias": medias, "title": "Website Name - {}".format(post.title)})


@login_required
def post_answer(request, post_id):
    if request.method == "POST":
        user = request.user
        text = request.POST['text']
        parent_sno = request.POST.get('parentSno', None)
        if parent_sno is not None:
            post = Post.objects.get(post_id=post_id)
            parent_answer = Answer.objects.get(id=parent_sno)
            customer_user = CustomUser.objects.get(user=user)
            answer = Answer(text=text, user=customer_user,
                            post=post, parent=parent_answer)
            answer.save()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            post = Post.objects.get(post_id=post_id)
            customer_user = CustomUser.objects.get(user=user)
            answer = Answer(text=text, user=customer_user, post=post)
            answer.save()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def delete_answer(request, answer_id):
    if request.method == "GET":
        user = request.user
        custom_user = CustomUser.objects.get(user=user)
        try:
            answer = Answer.objects.get(id=answer_id)
        except:
            answer = None
        if answer is not None and answer.user == custom_user:
            answer.delete()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, "Permission denied!")
            return redirect("/")


@login_required
def view_saved(request, page_number):
    try:
        if request.method == "GET":
            user_data = CustomUser.objects.get(
                user=request.user)
            offset = (int(page_number)*10)-10  # number of entry to leave
            limits = int(page_number)*10  # number of entry limit
            user = request.user
            custom_user = CustomUser.objects.get(user=user)
            saved_posts = Vault.objects.filter(user=custom_user)[offset:limits]
            posts = [saved.post for saved in saved_posts]
            posts_data = []
            last_entry = Vault.objects.filter(user=custom_user).last()
            is_last_page = False
            if last_entry is not None:
                try:
                  if last_entry.post == (list(posts))[-1]:
                      is_last_page = True
                except IndexError:
                  is_last_page = True
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
                data['username'] = post.username()
                data['profile_picture_link'] = post.author.profile_picture_link
                posts_data.append(data)
            if len(posts_data) == 0:
                is_last_page = True
                # send the data to home page as well
            return render(request, "saved_items.html", {"posts_data": posts_data, "user_data": user_data, "next_page": int(page_number)+1, "is_last_page": is_last_page})
        else:
            # if the user is unauthenticated
            messages.warning(request, "Only Registered user allowed")
            return redirect("/account/signup")
    except Exception as ex:
        print("Saved Vault Route: ", ex)
        return redirect("/account/signup")


@login_required
def blank_route_tag(request, tag):
    return redirect("/post/tag/{}/1".format(tag))


@login_required
def view_by_tag(request, tag, page_number):
    if request.method == "GET":
        offset = (int(page_number)*10)-10  # number of entry to leave
        limits = int(page_number)*10  # number of entry limit
        tags = Tags.objects.filter(text=tag)[offset:limits]
        posts = [tag.tag for tag in tags]
        posts_data = []
        user_data = CustomUser.objects.get(
            user=request.user)  # fetch the user from database
        last_entry = Tags.objects.filter(text=tag).last()
        try:
          is_last_page = True if last_entry.tag == posts[-1] else False
        except IndexError:
          is_last_page = True
        except AttributeError:
          is_last_page = True
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
                tags = [tagg.text for tagg in tags]
            except Tags.DoesNotExist:
                tags = []
            data['medias'] = medias
            data['post'] = post
            data['already_voted'] = already_voted
            data['tags'] = tags
            data['username'] = post.username()
            data['profile_picture_link'] = post.author.profile_picture_link
            posts_data.append(data)
            # send the data to home page as well

        return render(request, "home.html", {"user_data": user_data, "posts_data": (posts_data), "title": "Website Name - #{}".format(tag), "is_last_page": is_last_page})
