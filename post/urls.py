from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("create_post", views.create_post, name="create_post"),
    path("delete_post/<id>", views.delete_post, name="delete_post"),

]
