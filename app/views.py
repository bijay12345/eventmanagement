from django.shortcuts import render,get_object_or_404,redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (LikeSerializer,EventSerializer,EventCustomerSerializer,
	InterestSerializer,RatingSerializer,CommentSerializer,CommentSerializer2,ArticleSerializer)
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.reverse import reverse
from .models import Events,Rating,Comment,Article
import json
from django.http import HttpResponseRedirect
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import BasicAuthentication
from django.contrib import messages
import datetime
from rest_framework.authtoken.models import Token
from django.core.paginator import Paginator
from eventhost.models import EventHost
from eventhost.serializers import EventHostSerializer
from datetime import datetime



class HomeView(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	permission_classes=[IsAuthenticated]
	def get(self, request,slug=None, format=None):
		if slug is not None:

			event=Events.objects.get(slug=slug)

			id=event.id
			comment=Comment.objects.all().filter(event=id)
			c_serializer=CommentSerializer2(comment,many=True)

			rated=False
			if Rating.objects.filter(user=request.user.id).exists() and Rating.objects.filter(event=event).exists():
				rated=True
			
			rated_=json.dumps(rated)

			serializer=EventSerializer(event)
			context={
			"event":serializer.data,
			"rated":rated_,
			"comments":c_serializer.data,
			"H_active":"active",
			}

			print(datetime.now())

			return Response(context,template_name="app/event-detail.html")
		else:

			events=Events.objects.all()
			serializer=EventSerializer(events,many=True)
			paginator=Paginator(serializer.data,20)
			page_number=request.GET.get("page")
			page_obj=paginator.get_page(page_number)

			context={
			"page_obj":page_obj,
			"events":serializer.data,
			"H_active":"active",
			}

			return Response(context,template_name="app/event-list.html")



class LikeView(APIView):
	permission_classes=[IsAuthenticated]
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
	permission_classes=[IsAuthenticated]	
	def post(self,request,slug=None,format=None):
		data=dict(request.POST.items())
		inteid=data['interest_id']
		event=get_object_or_404(Events,slug=data.get('interest_id'))
		data={
		"interested":request.user.id
		}
		serializer=InterestSerializer(event,data=data,partial=True)

		if event.interested.filter(id=request.user.id).exists():
			if serializer.is_valid(raise_exception=True):
				event.interested.remove(request.user)
				if slug is not None:
					return redirect("detail",slug=slug)
				return redirect("home")
		else:
			if serializer.is_valid(raise_exception=True):
				event.interested.add(request.user)
				if slug is not None:
					return redirect("detail",slug=slug)
				return redirect("home")

class RatingView(APIView):
	permission_classes=[IsAuthenticated]
	def post(self,request,format=None):

		d=request.data
		rating=d["star"]
		user=request.user
		event=get_object_or_404(Events,slug=d.get('item_id'))
		data_={
		"rating":rating,
		"user":user.id,
		"event":event.id,
		}

		serializer=RatingSerializer(data=data_)

		if serializer.is_valid(raise_exception=True):
			serializer.save()
			messages.success(request,f"Thank you for your valuable rating")
			return redirect("detail",slug=event.slug)
		else:
			messages.warning(request,f"please rate correctly")
			return redirect("detail",slug=event.slug)
		return redirect("detail",slug=event.slug)


def aboutus(request):
	return render(request,"app/about.html")


class ArticleView(APIView):
	template_name="app/article.html"
	renderer_classes = [TemplateHTMLRenderer]
	def get(self,reqest,format=None):

		recent_events=Events.objects.all()[:3]
		serializer=EventSerializer(recent_events,many=True)

		articles=Article.objects.get(id=1)
		articleSerializer=ArticleSerializer(articles)

		return Response({"recentevents":serializer.data,"articles":articleSerializer.data,"A_active":"active",})


class CommentApiView(APIView):

	def get(self,request,id=None,format=None):
		if id is not None:
			comment=Comment.objects.all().filter(event=id)
			serializer=CommentSerializer(comment,many=True)
			return Response({"comments":serializer.data})
		else:
			comments=Comment.objects.all()
			serializer=CommentSerializer(comments,many=True)
			return Response(serializer.data)


	def post(self,request,format=None):
		data=request.data  
		event_id=data.get("event_id")
		event=get_object_or_404(Events,slug=event_id)
		user=request.user.id
		comments=request.data.get("comment")

		data={
		"comment":comments,
		"event":event.id,
		"user":user,
		}

		serializer=CommentSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			print("saving comment...")
		else:
			print(serializer.errors)
		return redirect("detail",slug=event_id)




class EventBookingApi(APIView):
	renderer_classes=[TemplateHTMLRenderer]
	def get(self,request,id=None,format=None):
		eventhosts=EventHost.objects.get(id=id)
		serializer=EventHostSerializer(eventhosts)
		return Response({"data":serializer.data,"B_active":"active",},template_name="app/eventbooking.html")

	def post(self,request,format=None):
		data=dict(request.POST.items())

		functionname=data.get("functionname")
		user = request.user.id  
		description = data.get("description")
		contact=data.get("contact")
		location=data.get("location")
		email=data.get("email")
		managingfirm=data.get("managementid")
		manager=get_object_or_404(EventHost,id=managingfirm)
		evedate=data.get("date")

		context={
		"email":email,
		"function_name":functionname,
		"customers":user,
		"description":description,
		"contact":contact,
		"location":location,
		"managingfirm":manager.id,
		"evedate":evedate
		}

		serializer=EventSerializer(data=context)

		if serializer.is_valid():
			serializer.save()
			messages.success(request,f"Hii {request.user.name}! You have successfully booked an event, For more details please visit your profile.") 
		else:
			print(serializer.errors)

		return redirect("hosts")





def design2(request):
	return render(request,"app/design2.html")

def design3(request):
	return render(request,"app/design3.html")
