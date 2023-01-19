from .models import EventHost
from users.models import Host,User
from rest_framework import serializers

class EventHostSerializer(serializers.ModelSerializer):
	event_hosts=serializers.StringRelatedField()
	host=serializers.StringRelatedField()
	class Meta:
		model=EventHost
		fields="__all__"


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
