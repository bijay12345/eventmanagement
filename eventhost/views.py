from django.shortcuts import render,redirect,get_object_or_404
from .serializers import EventHostSerializer,HostUserSerializer,HostLoginSerializer,HostFeedbackSerializer
from rest_framework.views import APIView
from .models import EventHost,HostFeedback
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
			print(eventhosts.get_total_stars())


			events=Events.objects.all().filter(managingfirm=id)[:3]
			eventdata=EventSerializer(events,many=True)

			feedbacks=HostFeedback.objects.all()
			feedbackdata=HostFeedbackSerializer(feedbacks,many=True)

			hosted_events=eventhosts.managingfirm.all()
			feedbacks=HostFeedback.objects.all().filter(eventhost=eventhosts)


			customers=[]
			for event in hosted_events:
				customers.append(event.customers)

			
			feedbackcustomers=[]
			for feed in feedbacks:
				feedbackcustomers.append(feed.user)

			context={
			
			}


			return Response({"host":serializer.data,"events":eventdata.data,"feedbacks":feedbackdata.data,
							"customers":customers,"feedbackcustomers":feedbackcustomers,"H_active":"active"},
							template_name="eventhost/hostdetail.html")


		eventhosts=EventHost.objects.all()
		serializer=EventHostSerializer(eventhosts,many=True)
		return Response({"hosts":serializer.data,"H_active":"active"},template_name="eventhost/hosts.html")


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
				return redirect('hostform')
			else:
				messages.warning(request,f"incorrect login credential")
				return redirect('hostlogin')
		else:
			messages.error(request,f"please provide login credentials")
			return redirect('hostlogin')


class EventHostRegisterApi(APIView):
	renderer_classes=[TemplateHTMLRenderer]
	template_name="eventhost/hostform.html"
	def get(self,request,format=None):
		print(request.user)
		return Response({"msg":"ok","A_active":"active"})


	def post(self,request,format=None):
		data_=request.data
		
		data={
		"host":request.user.id,
		"management_name":data_["managementname"],
		"email":data_["email"],
		"phonenumber":data_["phonenumber"],
		"street":data_["street"],
		"city":data_["city"],
		"pincode":data_["pincode"],
		"state":data_["state"],
		"description":data_["description"],
		"price":data_["price"],
		"image":data_["image"],
		}
		serializer = EventHostSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			print("everything OK")
		else:
			print(serializer.errors)
		return redirect("hosts")


class FeedBackApi(APIView):
	def post(self,request,id,format=None):
		data=request.data
		
		print(data.get("star"))

		context={
		"feedback":data.get("feedback"),
		"eventhost":data.get("host"),
		"user":request.user.id,
		"stars":data.get("star"),
		}

		serializer = HostFeedbackSerializer(data=context)
		if serializer.is_valid():
			serializer.save()
			messages.success(request,"Thank you for your feedback")
			return redirect("host-detail", id=id)
		else:
			messages.error(request,"oops something went wrong. Please try again later")
			print(serializer.errors)
			return redirect("host-detail", id=id)

