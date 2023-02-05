from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login,logout
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny
from .models import Profile,User
from rest_framework.response import Response
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import (UserSerializer,LoginSerializer,ProfileSerializer,ProfileUserSerializer)
from app.models import Events
from app.serializers import EventSerializer

class UserRegistrationView(APIView):
	permission_classes=[AllowAny]
	renderer_classes = [TemplateHTMLRenderer]

	def get(self, request, format=None):
		return Response({"R_active":"active"},template_name="users/register.html")

	def post(self,request,format=None):
		data=request.data

		serializer=UserSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			name=serializer.data.get("name")
			messages.success(request,f"user with username {name} successfully created")
			return redirect("login")
		else:
			print(serializer.errors)
			messages.error(request,f"Invalid credentials, register with valid credentials")
			return redirect("register")


class UserLoginView(APIView):
	permission_classes=[AllowAny]
	renderer_classes = [TemplateHTMLRenderer]

	def get(self, request, format=None):
		if not request.user.is_authenticated:
			return Response({"LO_active":"active"},template_name="users/login.html")
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



class ProfileView(APIView):
	permission_classes=[IsAuthenticated]
	template_name="users/userprofile.html"
	renderer_classes = [TemplateHTMLRenderer]

	def get(self,request,format=None):
		profile=get_object_or_404(Profile,user=request.user.id)
		user = get_object_or_404(User,id=request.user.id)

		profile_serializer=ProfileSerializer(profile)
		user_serializer=ProfileUserSerializer(user)

		eventbooked=Events.objects.all().filter(customers=request.user.id)
		events=EventSerializer(eventbooked,many=True)		

		return Response({"profiledata":profile_serializer.data,"userdata":user_serializer.data,"events":events.data,"P_active":"active"})

	def post(self,request,format=None):
		profile=get_object_or_404(Profile,user=request.user.id)
		user = get_object_or_404(User,id=request.user.id)

		print(request.data)

		data=request.data
		name=data.get("username")
		email=data.get("email")
		phonenumber=data.get("phonenumber")
		bio=data.get("bio")
		location=data.get("location")

		userdata={
		"name":name,
		"email":email
		}
		profile_data={
		"phonenumber":phonenumber,
		"bio":bio,
		"location":location,
		}

		userSerializer=ProfileUserSerializer(user,data=userdata,partial=True)
		profile_serializer=ProfileSerializer(profile,data=profile_data,partial=True)

		if userSerializer.is_valid():
			userSerializer.save()
			messages.success(request,f"{user.name}'s profile successfully updated!")
		else:
			print(userSerializer.errors)

		if profile_serializer.is_valid():
			profile_serializer.save()
			messages.success(request,f"{user.name}'s profile successfully updated!")
		else:
			print(profile_serializer.errors)

		return redirect("profile")

class profilePicUpdate(APIView):
	def post(self,request,format=None):
		profile=get_object_or_404(Profile,user=request.user.id)
		data=dict(request.POST.items())
		print(data)
		return Response({"msg":data})