from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from django.shortcuts import render,redirect
from django.contrib import messages

@login_required
def home(request):
  """this views is called when the user hits the route domain/home"""
  try:
    if request.user.is_authenticated and not request.user.is_superuser:
      data = CustomUser.objects.get(user=request.user) #fetch the user from database
      return render(request, "home.html", {"data": data}) #send the data to home page as well
    else:
      #if the user is unauthenticated
      messages.warning(request, "Only Registered user allowed")
      return redirect("/auth/signup")
  except Exception as ex:
    print("Home Route: ",ex)
    return redirect("/auth/signup")
