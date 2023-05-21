from django.db import models
from django.core.validators import MaxValueValidator
from PIL import Image
from django.template.defaultfilters import slugify
from users.models import User
from eventhost.models import EventHost
import datetime

class Events(models.Model):
	function_name=models.CharField(max_length=500)
	customers = models.ForeignKey(User,on_delete=models.CASCADE, related_name="customers")
	managingfirm=models.ForeignKey(EventHost,on_delete=models.CASCADE,related_name="managingfirm")
	location=models.CharField(max_length=100)
	contact=models.CharField(max_length=10)
	email=models.EmailField(max_length=200)
	evedate= models.DateField()
	bookingdate=models.DateField(auto_now_add=True)
	description=models.TextField()
	slug=models.CharField(max_length=1000,null=True,blank=True)
	likers=models.ManyToManyField(User,related_name='likers',blank=True)
	interested=models.ManyToManyField(User,related_name="interested",blank=True)
	image=models.ImageField(upload_to="articles",default="eventdefault.jpg")
	image2=models.ImageField(upload_to="articles",default="eventdefault.jpg")
	image3=models.ImageField(upload_to="articles",default="eventdefault.jpg")
	image4=models.ImageField(upload_to="articles",default="eventdefault.jpg")
	image5=models.ImageField(upload_to="articles",default="eventdefault.jpg")

	class Meta:
		ordering=['-evedate']


	def __str__(self):
		return self.function_name


	def save(self,*args,**kwargs):
		if not self.slug:
			self.slug=slugify(self.function_name+"-"+str(datetime.datetime.now()))
		return super().save(*args,**kwargs)


class Rating(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	event=models.ForeignKey(Events,on_delete=models.CASCADE)
	rating=models.IntegerField(validators=[MaxValueValidator(5)])

	def __str__(self):
		return self.user.name


class Comment(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="comment_user")
	event=models.ForeignKey(Events,on_delete=models.CASCADE,related_name="comments")
	comment=models.CharField(max_length=1000)
	date_commented=models.DateTimeField(auto_now_add=True)



	def __str__(self):
		return f"{self.user.name}: {self.event.function_name}"

	class Meta:
		ordering=['date_commented']



class Article(models.Model):
	image=models.ImageField(upload_to="articles",default="articledefault.jpg")
	heading = models.CharField(max_length=1000)
	quote=models.CharField(max_length=1000)
	workingmodel=models.ManyToManyField("WorkingModel")
	mission = models.ForeignKey("Mission",on_delete=models.SET_NULL,null=True,blank=True)

	def __str__(self):
		return f"{self.heading}"

class WorkingModel(models.Model):
	heading=models.CharField(max_length=100)
	quote=models.TextField()
	description=models.TextField()

	def __str__(self):
		return f"{self.heading}"

class Mission(models.Model):
	heading=models.CharField(max_length=1000)
	text=models.TextField()

	def __str__(self):
		return f"{self.heading}"
