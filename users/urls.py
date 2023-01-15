from django.urls import path
from .views import UserRegistrationView,UserLoginView,ProfileView,profilePicUpdate
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("register/",UserRegistrationView.as_view(),name="register"),
    path("login/",UserLoginView.as_view(),name="login"),
    path("logout/",LogoutView.as_view(template_name="users/logout.html"),name="logout"),
    path("profile/",ProfileView.as_view(),name="profile"),
    path("profile/pic/update/",profilePicUpdate.as_view(),name="profile_picUpdate"),
]
