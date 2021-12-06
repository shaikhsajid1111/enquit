from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from django.shortcuts import render,redirect
from django.contrib import messages
from post.models import Images, Post

@login_required
def home(request):
  """this views is called when the user hits the route domain/home"""
  try:
    if request.user.is_authenticated and not request.user.is_superuser:
      user_data = CustomUser.objects.get(user=request.user) #fetch the user from database
      posts = Post.objects.all()[:10]
      posts_data = []
      for post in posts:
        data = {}
        try:
          images = Images.objects.filter(post=post)
        except Images.DoesNotExist:
          images = []
        data['images'] = images
        data['post'] = post
        posts_data.append(data)
      return render(request, "home.html", {"user_data": user_data,"posts_data":(posts_data)}) #send the data to home page as well
    else:
      #if the user is unauthenticated
      messages.warning(request, "Only Registered user allowed")
      return redirect("/auth/signup")
  except Exception as ex:
    print("Home Route: ",ex)
    return redirect("/auth/signup")
