from .views import EventHostApi,HostLoginView,HostRegistrationView
from django.urls import path


urlpatterns=[
	path("hosts/",EventHostApi.as_view(),name="hosts"),
	path("hosts/<int:id>/",EventHostApi.as_view(),name="host-detail"),
	path("hostlogin/",HostLoginView.as_view(),name="hostlogin"),
	path("host/register/",HostRegistrationView.as_view(),name="hostregister"),
]