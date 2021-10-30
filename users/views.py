from django.shortcuts import render
from users.models import CustomUser
from .utils import get_image,password_is_valid
from django.contrib import messages




def signUp(request):
  if request.method == "GET":
    return render(request,"signup.html")
  elif request.method == "POST":
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    gender = request.POST['gender']
    age = request.POST['age']
    if password == confirm_password:
      if password_is_valid(password):
        image = get_image(gender=gender,age=age)
        custom_user = CustomUser(email=email, profile_picture_link=image)
        custom_user.save()
        return render(request,"home.html")
      else:
        messages.error(request,"Password Must be above length of and Alphanumeric")
        return render(request,"signup.html")

