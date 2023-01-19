from django.shortcuts import render,redirect,get_object_or_404
from .serializers import EventHostSerializer,HostUserSerializer,HostLoginSerializer
from rest_framework.views import APIView
from .models import EventHost
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib import messages
from django.contrib.auth import authenticate,login
from app.models import Events
from app.serializers import EventSerializer

from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,DestroyAPIView,RetrieveAPIView



class EventHostApi(APIView):
	renderer_classes=[TemplateHTMLRenderer]
	def get(self,request,id=None,format=None):
		if id is not None:
			eventhosts=EventHost.objects.get(id=id)
			serializer=EventHostSerializer(eventhosts)
			events=Events.objects.all().filter(managingfirm=id)[:3]
			eventdata=EventSerializer(events,many=True)
			return Response({"host":serializer.data,"events":eventdata.data},template_name="eventhost/hostdetail.html")


		eventhosts=EventHost.objects.all()
		serializer=EventHostSerializer(eventhosts,many=True)
		return Response({"hosts":serializer.data},template_name="eventhost/hosts.html")





class HostRegistrationView(APIView):
	renderer_classes = [TemplateHTMLRenderer]

	def get(self, request, format=None):
		return Response(template_name="eventhost/hostregister.html")

	def post(self,request,format=None):
		data=request.data

		serializer=HostUserSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			name=serializer.data.get("name")
			messages.success(request,f"hostuser with username {name} successfully created")
			return redirect("hostlogin")
		else:
			print(serializer.errors)
			messages.error(request,f"Invalid credentials, register with valid credentials")
			return redirect("hostregister")




class HostLoginView(APIView):
	renderer_classes = [TemplateHTMLRenderer]

	def get(self, request, format=None):
		return Response(template_name="eventhost/hostlogin.html")

	def post(self,request,format=None):
		
		data=dict(request.POST.items())
		data_={
		"email":data["email"],
		"password":data["password"]
		}


		serializer=HostLoginSerializer(data=data_)
		if serializer.is_valid():
			email=serializer.data.get("email")
			password=serializer.data.get("password")
			user=authenticate(email=email,password=password)
			if user is not None:
				login(request,user)
				return redirect('hosts')
			else:
				messages.warning(request,f"incorrect login credential")
				return redirect('hostlogin')
		else:
			messages.error(request,f"please provide login credentials")
			return redirect('hostlogin')
