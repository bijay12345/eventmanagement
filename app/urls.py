from django.urls import path
from .views import UserRegistrationView,UserLoginView,HomeView,LikeView,InterestView,RatingView,ProfileView,aboutus
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("home/",HomeView.as_view(),name="home"),
    path("home/<int:id>/",HomeView.as_view(),name="detail"),
    path("register/",UserRegistrationView.as_view(),name="register"),
    path("",UserLoginView.as_view(),name="login"),
    path("like/",LikeView.as_view(),name="like"),
    path("like/<int:id>",LikeView.as_view(),name="detaillike"),
    path("interest/<int:id>",InterestView.as_view(),name="detailinterest"),
    path("interest/",InterestView.as_view(),name="interest"),
    path("rating/",RatingView.as_view(),name="rating"),
    path("logout/",LogoutView.as_view(template_name="app/logout.html"),name="logout"),
    path("profile/",ProfileView.as_view(),name="profile"),
    path("aboutus/",aboutus,name="about-us")
]
