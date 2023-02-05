from django.db import models
from PIL import Image
from users.models import Host,User
from django.core.validators import MaxValueValidator


class EventHost(models.Model):
	host=models.ForeignKey(Host,on_delete=models.CASCADE)
	management_name = models.CharField(max_length=300)
	email=models.EmailField(max_length=200)
	phonenumber=models.CharField(max_length=10)
	street=models.CharField(max_length=100)
	city=models.CharField(max_length=100)
	pincode=models.CharField(max_length=10)
	state=models.CharField(max_length=100)
	description=models.CharField(max_length=500)
	price=models.DecimalField(decimal_places=2,max_digits=8)
	image=models.ImageField(upload_to="hostImages",default="defaulthost.jpg")

	def __str__(self):
		return self.management_name

	def get_total_stars(self):
		feedbacks=HostFeedback.objects.all().filter(eventhost=self)
		totalstars=0  
		for star in feedbacks:
			totalstars+=star.stars
		return totalstars


class HostFeedback(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	eventhost=models.ForeignKey(EventHost,on_delete=models.CASCADE,related_name="host_feedback")
	feedback=models.TextField()
	stars=models.IntegerField(validators=[MaxValueValidator(5)])

	def __str__(self):
		return self.user.name


