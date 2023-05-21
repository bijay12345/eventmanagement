from rest_framework import serializers 
from .models import Events,Rating,Comment,Article,WorkingModel,Mission
from users.models import User
from datetime import date



class EventSerializer(serializers.ModelSerializer):
	likers=serializers.StringRelatedField(many=True,read_only=True)
	likers_count=serializers.SerializerMethodField()
	no_of_comments=serializers.SerializerMethodField()
	managingfirmname=serializers.SerializerMethodField()
	avgrating=serializers.SerializerMethodField()
	comments=serializers.StringRelatedField(many=True,required=False)
	no_of_interested=serializers.SerializerMethodField(required=False)
	eventdate=serializers.SerializerMethodField()
	bookingdate=serializers.SerializerMethodField()

	image = serializers.ImageField(
            max_length=None, use_url=True,required=False
        )
	image2 = serializers.ImageField(
            max_length=None, use_url=True,required=False
        )
	image3 = serializers.ImageField(
            max_length=None, use_url=True,required=False
        )
	image4 = serializers.ImageField(
            max_length=None, use_url=True,required=False
        )
	image5 = serializers.ImageField(
            max_length=None, use_url=True,required=False
        )


	def get_likers_count(self,obj):
		return obj.likers.count()


	def get_no_of_interested(self,obj):
		return obj.interested.count()

	def get_no_of_comments(self,obj):
		return obj.comments.count()

	def get_managingfirmname(self,obj):
		return obj.managingfirm.management_name

	def get_avgrating(self,obj):
		ratings=Rating.objects.filter(event=obj)
		count = len(ratings)
		sum = 0
		for rvw in ratings:
			sum += rvw.rating
		if sum == 0:
			return 0
		s=sum/count
		return round(s,1)


	def get_eventdate(self,obj):
		return obj.evedate

	def get_bookingdate(self,obj):
		return obj.bookingdate


	class Meta:
		model=Events
		fields='__all__'





class LikeSerializer(serializers.ModelSerializer):
	likers=serializers.StringRelatedField(many=True,read_only=True)
	class Meta:
		model=Events 
		fields=["likers"]
		

class InterestSerializer(serializers.ModelSerializer):
	interested=serializers.StringRelatedField(many=True,read_only=True)

	class Meta:
		model=Events 
		fields=["interested"]
	
	
class RatingSerializer(serializers.ModelSerializer):
	class Meta:
		model=Rating
		fields=["user","event","rating"]


class CommentSerializer(serializers.ModelSerializer):
	event=serializers.PrimaryKeyRelatedField(queryset=Events.objects.all())
	user=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

	class Meta:
		model=Comment  
		fields = ["user","event","comment"]


class CommentSerializer2(serializers.ModelSerializer):
	event=serializers.StringRelatedField(read_only=True)
	user=serializers.StringRelatedField(read_only=True)
	date_comment=serializers.SerializerMethodField()

	def get_date_comment(self,obj):
		date = obj.date_commented
		return date

	class Meta:
		model=Comment  
		fields = ["user","event","comment","date_comment"]


class EventCustomerSerializer(serializers.ModelSerializer):
	class Meta:
		model=Events
		fields=["customers","managingfirm","functionname","description","contact","location","email"]



class MissionSerializer(serializers.ModelSerializer):
	class Meta:
		model=Mission
		fields=["heading","text"]

class ArticleSerializer(serializers.ModelSerializer):
	image = serializers.ImageField(max_length=None, use_url=True,required=False)
	workingmodel=serializers.PrimaryKeyRelatedField(queryset=WorkingModel.objects.all())
	mission=MissionSerializer(read_only=True)
	class Meta:
		model=Article
		fields=["id","image","heading","quote","workingmodel","mission"]