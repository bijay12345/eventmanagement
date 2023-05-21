from rest_framework import serializers 
from .models import User,Profile


class UserSerializer(serializers.ModelSerializer):
	password2=serializers.CharField(style={"input_type":"password"},write_only=True)
	class Meta:
		model=User
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
		return User.objects.create_user(**validate_data)


class LoginSerializer(serializers.ModelSerializer):
	email=serializers.EmailField(max_length=255)
	class Meta:
		model=User  
		fields=['email','password']



class ProfileSerializer(serializers.ModelSerializer):
	image = serializers.ImageField(
            max_length=None, use_url=True
        )
	phonenumber=serializers.CharField()
	class Meta:
		model=Profile
		fields=['image','phonenumber','location','bio']


class ProfileUserSerializer(serializers.ModelSerializer):
	email=serializers.EmailField(max_length=255)
	name=serializers.CharField(max_length=100)
	class Meta:
		model=User
		fields=["name","email"]