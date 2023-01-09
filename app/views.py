from django.shortcuts import render,get_object_or_404,redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import (UserSerializer,LoginSerializer,LikeSerializer,EventSerializer,
	InterestSerializer,RatingSerializer,ProfileSerializer,ProfileUserSerializer)
from django.contrib.auth import authenticate,login,logout
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.reverse import reverse
from .models import Events,Rating,Profile,User
import json
from django.http import HttpResponseRedirect
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import BasicAuthentication
from django.contrib import messages
from rest_framework.parsers import FileUploadParser
import datetime
from rest_framework.authtoken.models import Token

class HomeView(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	def get(self, request,id=None, format=None):
		if id is not None:
			
			event=Events.objects.get(id=id)

			rated=False
			if Rating.objects.filter(user=request.user.id).exists() and Rating.objects.filter(event=event).exists():
				rated=True

			avgrating=event.avgrating()
			intersted_people=event.no_of_interested_count()
			no_of_likes=event.no_of_likes()
			
			rated_=json.dumps(rated)
			avgrating=json.dumps(avgrating)
			intersted_people=json.dumps(intersted_people)
			no_of_likes=json.dumps(no_of_likes)

			serializer=EventSerializer(event)
			context={
			"event":serializer.data,
			"rated":rated_,
			"avgrating":avgrating,
			"intersted_people":intersted_people,
			"no_of_likes":no_of_likes,
			}

			return Response(context,template_name="app/event-detail.html")
		else:
			dates=datetime.date.today()
			events=Events.objects.all()

			serializer=EventSerializer(events,many=True)
			context={
			"events":serializer.data,
			}
			return Response(context,template_name="app/design-list.html")


class UserRegistrationView(APIView):
	permission_classes=[AllowAny]
	renderer_classes = [TemplateHTMLRenderer]

	def get(self, request, format=None):
		return Response(template_name="app/register.html")

	def post(self,request,format=None):
		data=dict(request.POST.items())
		data_={
		"email":data["email"],
		"name":data["username"],
		"password":data["password"],
		"password2":data["password2"]
		}
		serializer=UserSerializer(data=data_)
		if serializer.is_valid():
			serializer.save()
			name=serializer.data.get("name")
			messages.success(request,f"user with username {name} successfully created")
			return redirect("login")
		else:
			print(serializer.errors)
			return redirect("register")
		return Response(template_name="app/register.html")

class UserLoginView(APIView):
	permission_classes=[AllowAny]
	renderer_classes = [TemplateHTMLRenderer]

	def get(self, request, format=None):
		if not request.user.is_authenticated:
			return Response(template_name="app/login.html")
		else:
			return redirect('home')

	def post(self,request,format=None):
		
		data=dict(request.POST.items())
		data_={
		"email":data["email"],
		"password":data["password"]
		}

		serializer=LoginSerializer(data=data_)
		if serializer.is_valid():
			email=serializer.data.get("email")
			password=serializer.data.get("password")
			user=authenticate(email=email,password=password)
			if user is not None:
				login(request,user)
				return redirect('home')
			else:
				messages.warning(request,f"incorrect login credential")
				return redirect('login')
		else:
			messages.error(request,f"please provide login credentials")
			return redirect('login')
		messages.error(request,f"please login first")
		return Response(template_name="app/login.html")



class LikeView(APIView):
	def post(self,request,id=None,format=None):
		data=dict(request.POST.items())
		eveid=data['event_id']
		event=get_object_or_404(Events,id=data.get('event_id'))
		data={
		"likers":request.user.id
		}
		serializer=LikeSerializer(event,data=data,partial=True)
		if event.likers.filter(id=request.user.id).exists():
			if serializer.is_valid(raise_exception=True):
				event.likers.remove(request.user)
				if id is not None:
					return redirect("detail",id=eveid)
				else:
					return redirect("home")
		else:
			if serializer.is_valid(raise_exception=True):
				event.likers.add(request.user)
				if id is not None:
					return redirect("detail",id=eveid)
				else:
					return redirect("home")


class InterestView(APIView):
	def post(self,request,id=None,format=None):
		data=dict(request.POST.items())
		inteid=data['interest_id']
		event=get_object_or_404(Events,id=data.get('interest_id'))
		data={
		"likers":request.user.id
		}
		serializer=InterestSerializer(event,data=data,partial=True)
		if event.interested.filter(id=request.user.id).exists():
			if serializer.is_valid(raise_exception=True):
				event.interested.remove(request.user)
				if id is not None:
					return redirect("detail",id=inteid)
				else:
					return redirect("home")
		else:
			if serializer.is_valid(raise_exception=True):
				event.interested.add(request.user)
				if id is not None:
					return redirect("detail",id=inteid)
				else:
					return redirect("home")

class RatingView(APIView):

	def post(self,request,format=None):

		d=request.data
		rating=d["star"]
		user=request.user
		event=get_object_or_404(Events,id=d.get('item_id'))
		data_={
		"rating":rating,
		"user":user.id,
		"event":event.id,
		}

		serializer=RatingSerializer(data=data_)

		if serializer.is_valid(raise_exception=True):
			serializer.save()
			messages.success(request,f"Thank you for your valuable rating")
			return redirect("detail",id=event.id)
		else:
			messages.warning(request,f"please rate correctly")
			return redirect("detail",id=event.id)
		return redirect("detail",id=event.id)


	
class ProfileView(APIView):

	template_name="app/userprofile.html"
	renderer_classes = [TemplateHTMLRenderer]

	def get(self,request,format=None):
		profile=get_object_or_404(Profile,user=request.user.id)
		user = get_object_or_404(User,id=request.user.id)

		profile_serializer=ProfileSerializer(profile)
		user_serializer=ProfileUserSerializer(user)

		return Response({"profiledata":profile_serializer.data,"userdata":user_serializer.data})

	def post(self,request,format=None):
		profile=get_object_or_404(Profile,user=request.user.id)
		user = get_object_or_404(User,id=request.user.id)

		data=request.data

		name=data.get("username")
		email=data.get("email")
		image=data.get("image")
		userdata={
		"name":name,
		"email":email
		}
		profiledata={
		"image":image,
		}
		userSerializer=ProfileUserSerializer(user,data=userdata)
		profile_serializer=ProfileSerializer(profile,data=profiledata)

		if userSerializer.is_valid():
			userSerializer.save()
			messages.success(request,f"{user.name}'s profile successfully updated!")

		if profile_serializer.is_valid():
			profile_serializer.save()
			messages.success(request,f"{user.name}'s profile successfully updated!")

		messages.warning(request,"Please input some data to post")
		return redirect("profile")


def aboutus(request):
	return render(request,"app/about.html")


def design(request):
	return render(request,"app/design.html")

def design2(request):
	return render(request,"app/design2.html")

def design3(request):
	return render(request,"app/design3.html")
