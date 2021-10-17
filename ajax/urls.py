from django.urls import path
from . import views


#all ajax routes are registered here
urlpatterns = [
  path("fetch_posts",views.fetch_posts)
  ]