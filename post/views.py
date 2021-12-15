from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from .models import Post, Images, Answer, Vault
import cloudinary  # external library
import cloudinary.uploader  # external library


@login_required(login_url="/account/login")
def create_post(request):
    if request.method == "GET":
        return render(request, "create_post.html")
    if request.method == "POST":
        text = request.POST['text']
        images = request.FILES.getlist('images')

        user = CustomUser.objects.get(user=request.user)
        post = Post(text=text, author=user)
        post.save()
        for image in images:
            if post is not None:
                result = cloudinary.uploader.upload(image)
                print(result)
                image_obj = Images.objects.create(
                    url=result["url"], public_id=result['public_id'], post=post)
        post.save()
        messages.success(request, "Post Created Successfully!")
        return redirect("/")


@login_required(login_url="/account/login")
def delete_post(request, id):
    if request.method == "GET":
        try:
            post = Post.objects.get(post_id=id)
        except Post.DoesNotExist:
            post = None
        if post is None:
            messages.error(request, "Post Does Not Exists!")
            return redirect("/")
        elif request.user.id != post.author.id:
            messages.error(request, "Permission Denied!")
            return redirect("/")
        else:
            images = Images.objects.filter(post=post)
            for image in images:
                cloudinary.uploader.destroy(image.public_id)
            post.delete()
            messages.success(request, "Post deleted!")
            return redirect("/")


@login_required(login_url="/account/login")
def view_post(request, post_id):
    if request.method == "GET":
        post = Post.objects.get(post_id=post_id)
        answers = Answer.objects.filter(post=post, parent=None)
        data = []
        for answer in answers:
            temp_data = {}
            temp_data['answer'] = answer
            replies_list = []
            try:
                replies = Answer.objects.filter(parent=answer)
            except:
                replies = []
            for reply in replies:
                replies_list.append(reply)
            temp_data['replies'] = replies_list
            data.append(temp_data)
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
            return redirect("/")
        else:
            post = Post.objects.get(post_id=post_id)
            customer_user = CustomUser.objects.get(user=user)
            answer = Answer(text=text, user=customer_user, post=post)
            answer.save()
        return redirect("/")


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
            return redirect("/")
        else:
            messages.error(request, "Permission denied!")
            return redirect("/")


@login_required
def view_saved(request):
    if request.method == "GET":
        user = request.user
        custom_user = CustomUser.objects.get(user=user)
        saved_posts = Vault.objects.filter(user=custom_user)
        return render(request,"home.html",{"posts_data":saved_posts,"user_data":custom_user})
