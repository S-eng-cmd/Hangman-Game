from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html", next_page="index"
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="index"), name="logout"),
    path("signup/", views.signup, name="signup"),
    path("start/", views.start_game, name="start_game"),
    path("game/<int:game_id>", views.play_game, name="play_game"),
]
