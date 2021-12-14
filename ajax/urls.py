from django.urls import path
from . import views


# all ajax routes are registered here
urlpatterns = [
    path("fetch_posts", views.fetch_posts),
    path("vote_post/<post_id>", views.vote_post),
    path("report_post/<post_id>", views.report_post),
    path("vote_answer/<answer_id>", views.vote_answer),
    path("save/<post_id>", views.save_answer)
]
