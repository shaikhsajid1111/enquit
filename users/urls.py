from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("signup", views.signUp, name="signup"),
    path("login", views.login_user, name="login"),
    path("logout", views.log_out, name="logout"),
    path("delete", views.delete_user, name="delete_user"),

    path("view/<username>/<page_number>", views.view_user, name="view_user"),
    path("view/<username>", views.blank_route_view_user, name="view_user_blank"),

    # views to activate account
    path("activate/<uid64>/<token>", views.activate, name="activate"),

    # views to change or reset password

    path("password_reset", auth_views.PasswordResetView.as_view(
        template_name="password_reset.html"), name="password_reset"),
    path("password_reset/done", auth_views.PasswordResetDoneView.as_view(
        template_name="password_reset_done.html"), name="password_reset_done"),

    path("reset/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done", auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),


]
