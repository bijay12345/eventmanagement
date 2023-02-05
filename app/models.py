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
	image=models.ImageField(upload_to='eventpic',default='default.jpeg')
	image2=models.ImageField(upload_to='eventpic',default='default.jpeg')
	image3=models.ImageField(upload_to='eventpic',default='default.jpeg')
	image4=models.ImageField(upload_to='eventpic',default='default.jpeg')
	image5=models.ImageField(upload_to='eventpic',default='default.jpeg')

	class Meta:
		ordering=['-evedate']


	def __str__(self):
		return self.function_name


	def save(self,*args,**kwargs):
		if not self.slug:
			self.slug=slugify(self.function_name+"-"+str(datetime.datetime.now()))
		
		image=Image.open(self.image.path)
		image2=Image.open(self.image2.path)
		image3=Image.open(self.image3.path)
		image4=Image.open(self.image4.path)
		image5=Image.open(self.image5.path)

		if image.width > 500 or image.height > 500:
			output=(500,500)
			image.thumbnail(output)
			image.save(self.image.path)

		if image2.width > 500 or image2.height > 500:
			output=(500,500)
			image2.thumbnail(output)
			image2.save(self.image2.path)

		if image3.width > 500 or image3.height > 500:
			output=(500,500)
			image3.thumbnail(output)
			image3.save(self.image3.path)

		if image4.width > 500 or image4.height > 500:
			output=(500,500)
			image4.thumbnail(output)
			image4.save(self.image4.path)

		if image5.width > 500 or image5.height > 500:
			output=(500,500)
			image5.thumbnail(output)
			image5.save(self.image5.path)

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





