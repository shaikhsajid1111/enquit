from django.urls import path
from . import views


# all API routes are registered here
urlpatterns = [
    path("fetch_posts/<page_number>", views.fetch_posts),
    path("vote_post/<post_id>", views.vote_post),
    path("report_post/<post_id>", views.report_post),
    path("vote_answer/<answer_id>", views.vote_answer),
    path("save/<post_id>", views.save_answer),
    path("fetch_user_posts/<username>/<page_number>", views.fetch_user_posts),
    path("delete_answer/<answer_id>", views.delete_answer),
    path("fetch_post_answers/<post_id>/<page_number>", views.fetch_answers),
    path("fetch_saved_posts/<page_number>", views.fetch_saved_posts),
    path("report_answer/<answer_id>", views.report_answer),
    path("fetch_search_result/<query>/<page_number>",views.fetch_search_result),
    path("fetch_by_tag/<tag>/<page_number>", views.fetch_posts_by_tag),
    path("report_account/<account_id>", views.report_account),
    path("fetch_answer_replies/<parent_id>/<page_number>", views.fetch_answer_replies),

]
