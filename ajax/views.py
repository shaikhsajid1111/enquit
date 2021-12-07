from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
import json
from users.models import CustomUser
from post.models import Post,Vote,Report, Images
from django.contrib.auth.decorators import login_required
import cloudinary
import cloudinary.uploader

def fetch_posts(request):
  return JsonResponse({"name":"sajid"},content_type="application/json",safe=False)

@login_required
def vote_post(request,post_id):
  if request.method == "POST":
    user = CustomUser.objects.get(user=request.user)
    post = Post.objects.get(post_id=post_id)
    new_vote, created = Vote.objects.get_or_create(user=user,post=post)
    return JsonResponse({"Liked":True})

@login_required
def report_post(request,post_id):
  if request.method == "POST":
    user = CustomUser.objects.get(user=request.user)
    post = Post.objects.get(post_id=post_id)
    new_report, created = Report.objects.get_or_create(user=user,post=post)
    report_counts = Report.objects.filter(post=post).count()
    number_of_users = CustomUser.objects.all().count()
    print("Percentage: ", (2/100)*number_of_users)
    if report_counts > (2/100)*number_of_users:
      images = Images.objects.filter(post=post)
      for image in images:
        cloudinary.uploader.destroy(image.public_id)
      post.delete()
    return JsonResponse({"Reported":True})


