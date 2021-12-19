from os import name
from django.urls import path

from api.views import delete_answer
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("create_post", views.create_post, name="create_post"),
    path("saved", views.view_saved, name="saved"),
    path("delete_post/<id>", views.delete_post, name="delete_post"),
    path("view/<post_id>", views.view_post, name="view_post"),
    path("view/post_comment/<post_id>", views.post_answer, name="post_comment"),

    path("delete_answer/<answer_id>", views.delete_answer, name="delete_answer"),
    path("tag/<tag>",views.view_by_tag,name="tag_view")
]
