from rest_framework import serializers 
from .models import Events,Rating,Comment
from users.models import User

class EventSerializer(serializers.ModelSerializer):
	likers=serializers.StringRelatedField(many=True,read_only=True)
	likers_count=serializers.SerializerMethodField()
	avgrating=serializers.SerializerMethodField()
	comments=serializers.StringRelatedField(many=True)
	no_of_interested=serializers.SerializerMethodField()

	image = serializers.ImageField(
            max_length=None, use_url=True
        )
	image2 = serializers.ImageField(
            max_length=None, use_url=True
        )
	image3 = serializers.ImageField(
            max_length=None, use_url=True
        )
	image4 = serializers.ImageField(
            max_length=None, use_url=True
        )
	image5 = serializers.ImageField(
            max_length=None, use_url=True
        )


	def get_likers_count(self,obj):
		return obj.likers.count()


	def get_no_of_interested(self,obj):
		return obj.interested.count()



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
	date_commented=serializers.DateTimeField()
	class Meta:
		model=Comment  
		fields = ["user","event","comment","date_commented"]