from django.urls import path
from . import views

urlpatterns = [
path("signup",views.signUp,name="signup"),
path("login",views.login_user,name="login"),
path("logout",views.log_out,name="logout"),
path("delete",views.delete_user,name="delete_user"),


]