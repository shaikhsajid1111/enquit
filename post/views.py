from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from .models import Post, Images
import cloudinary
import cloudinary.uploader


@login_required(login_url="/auth/login")
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
                    url=result["url"],public_id=result['public_id'], post=post)
        post.save()
        messages.success(request, "Post Created Successfully!")
        return redirect("/home")

@login_required(login_url="/auth/login")
def delete_post(request,id):
  if request.method == "GET":
    try:
      post = Post.objects.get(post_id=id)
    except Post.DoesNotExist:
      post = None
    if post is None:
      messages.error(request, "Post Does Not Exists!")
      return redirect("/home")
    elif request.user.id != post.author.id:
      messages.error(request, "Permission Denied!")
      return redirect("/home")
    else:
      images = Images.objects.filter(post=post)
      for image in images:
        cloudinary.uploader.destroy(image.public_id)
      post.delete()
      messages.success(request, "Post deleted!")
      return redirect("/home")
