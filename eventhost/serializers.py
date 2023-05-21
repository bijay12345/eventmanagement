from .models import EventHost,HostFeedback
from users.models import Host,User
from rest_framework import serializers

class EventHostSerializer(serializers.ModelSerializer):
	image = serializers.ImageField(
            max_length=None, use_url=True,required=False
        )
	total_stars=serializers.SerializerMethodField()

	def get_total_stars(self,obj):
		feedbacks=HostFeedback.objects.all().filter(eventhost=obj)
		totalusers=len(feedbacks)

		totalstars=0  
		for star in feedbacks:
			totalstars+=star.stars
		return (totalstars/totalusers)

	class Meta:
		model=EventHost
		fields=['id','host','management_name','email','phonenumber','street','city','pincode','state','description','price',"image","total_stars"]


class HostLoginSerializer(serializers.ModelSerializer):
	email=serializers.EmailField(max_length=255)
	class Meta:
		model=Host  
		fields=['email','password']


class HostUserSerializer(serializers.ModelSerializer):
	password2=serializers.CharField(style={"input_type":"password"},write_only=True)
	class Meta:
		model=Host
		fields=["email","name","password","password2"]
		extra_kwargs={
		"password":{"write_only":True}
		}

	def validate(self,data):
		password=data.get("password")
		password2=data.get("password2")
		if password != password2:
			raise serializers.ValidationError("Passwords doesn't match")
		return data

	def create(self,validate_data):
		return Host.objects.create_user(**validate_data)

class HostFeedbackSerializer(serializers.ModelSerializer):
	user_image = serializers.SerializerMethodField()
	user_name = serializers.SerializerMethodField()

	

	def get_user_image(self,obj):
		return obj.user.profile.image.url

	def get_user_name(self,obj):
		return obj.user.name



	class Meta:
		model=HostFeedback
		fields="__all__"


