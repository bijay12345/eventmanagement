from django.urls import path
from .views import HomeView,LikeView,InterestView,RatingView,aboutus,ArticleView,design3,design2,CommentApiView,EventBookingApi
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("home/",HomeView.as_view(),name="home"),
    path("home/<str:slug>/",HomeView.as_view(),name="detail"),
    path("like/",LikeView.as_view(),name="like"),
    path("like/<int:id>",LikeView.as_view(),name="detaillike"),
    path("interest/<str:slug>",InterestView.as_view(),name="detailinterest"),
    path("interest/",InterestView.as_view(),name="interest"),
    path("rating/",RatingView.as_view(),name="rating"),
    path("aboutus/",aboutus,name="about-us"),
    path("",ArticleView.as_view(),name="front"),
    path("design2/",design2,name="design2"),
    path("design3/",design3,name="design3"),
    path('comments/',CommentApiView.as_view(),name="comments"),
    path("comments/<int:id>/",CommentApiView.as_view(),name="comment"),
    path("eventbooking/<int:id>",EventBookingApi.as_view(),name="eventbooking"),
    path("eventbooking/",EventBookingApi.as_view(),name="eventbooking-post")
]
