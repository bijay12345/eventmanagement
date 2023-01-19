from django.db import models
from PIL import Image
from users.models import Host,User



class EventHost(models.Model):
	host=models.ForeignKey(Host,on_delete=models.CASCADE)
	management_name = models.CharField(max_length=300)
	location=models.CharField(max_length=200)
	description=models.CharField(max_length=500)
	price=models.DecimalField(decimal_places=2,max_digits=8)

	def __str__(self):
		return self.management_name


class HostImages(models.Model):
	event=models.OneToOneField(EventHost,on_delete=models.CASCADE,related_name="event_hosts")
	images=models.ImageField(upload_to="hostImages")

	def __str__(self):
		return self.images.path

