from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from .models import Post, Medias, Answer, Vault, Tags, Vote
import cloudinary  # external library
import cloudinary.uploader  # external library
from django.http import HttpResponseRedirect

@login_required(login_url="/account/login")
def create_post(request):
    """function to create post"""
    if request.method == "GET":
      #if GET request then render its HTML
        return render(request, "create_post.html")
    if request.method == "POST":
        #extract respective content from the request
        text = request.POST['text']
        medias = request.FILES.getlist('medias')
        tags = request.POST['tags']
        user = CustomUser.objects.get(user=request.user)
        post = Post(text=text, author=user) #create post
        post.save()
        for media in medias:
          #upload media to the cloudinary server
            if post is not None:
                result = cloudinary.uploader.upload_large(media) #upload
                #create object for the uploaded file
                media_obj = Medias.objects.create(
                    url=result["url"], public_id=result['public_id'], post=post)
        post.save() #save to the DB
        for tag in tags.split(" "):
            #split out tags from the given tags
            tag_obj = Tags.objects.create(text=tag, tag=post) #create tag obj
            tag_obj.save() #save

        messages.success(request, "Post Created Successfully!") #send success message to the front-end
        return redirect("/")


@login_required(login_url="/account/login")
def delete_post(request, id):
    """function to delete post"""
    if request.method == "GET":
        try:
            #try to find the post
            post = Post.objects.get(fid=id)
        except Post.DoesNotExist:
            #if post does not exists, set it to None
            post = None
        if post is None:
            #if post was not found
            messages.error(request, "Post Does Not Exists!") #send error to front-end
            return redirect("/") #redirect to the homepage
        elif request.user.id != post.author.id:
          #if someone is trying to delete someone else's post
            messages.error(request, "Permission Denied!") #send error message to front-end
            return redirect("/")
        else:
            #if no problem occured, delete the post
            medias = Medias.objects.filter(post=post)
            for media in medias:
                #delete all the media of the post
                cloudinary.uploader.destroy(media.public_id)
            post.delete() #delete the post
            messages.success(request, "Post deleted!")
            return redirect("/") #to the home page


@login_required(login_url="/account/login")
def view_post(request, post_id):
    """function to view post"""
    if request.method == "GET":
        post = Post.objects.get(post_id=post_id) #find the post

        #find all parent answers, exclude the replies for the answer hence the "parent=None" was passed
        answers = Answer.objects.filter(post=post, parent=None)
        data = []
        for answer in answers:
            #traverse through all answers and find their replies as well
            temp_data = {}
            temp_data['answer'] = answer
            replies_list = []
            try:
                #find all replies to the parent answer
                replies = Answer.objects.filter(parent=answer)
            except:
                #if error occurs in finding
                replies = []
            for reply in replies:
                #traverse over the replies and save it to the list
                replies_list.append(reply)
            temp_data['replies'] = replies_list
            data.append(temp_data) #append the dict into the list
        return render(request, "post_details.html", {"post_data": post, "answers": data})


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
def view_saved(request):
    if request.method == "GET":
        user = request.user
        custom_user = CustomUser.objects.get(user=user)
        saved_posts = Vault.objects.filter(user=custom_user)
        return render(request, "home.html", {"posts_data": saved_posts, "user_data": custom_user})


@login_required
def view_by_tag(request, tag):
    if request.method == "GET":
        tags = Tags.objects.filter(text=tag)
        posts = [tag.tag for tag in tags]
        posts_data = []
        user_data = CustomUser.objects.get(
            user=request.user)  # fetch the user from database
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
            posts_data.append(data)
            # send the data to home page as well
            return render(request, "home.html", {"user_data": user_data, "posts_data": (posts_data), "title": "Website Name - {}".format(tag)})
