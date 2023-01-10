from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import MaxValueValidator
from PIL import Image
from django.template.defaultfilters import slugify

class UserManager(BaseUserManager):
	def create_user(self,email,name,password=None,password2=None):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
				email=self.normalize_email(email),
				name=name,	
			)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self,email,name,password=None):
		user=self.create_user(
				email,
				password=password,
				name=name,
			)
		user.is_admin=True  
		user.save(using=self._db)
		return user


class User(AbstractBaseUser):
	email=models.EmailField(verbose_name="Email Address",
		max_length=255,
		unique=True
		)
	name=models.CharField(max_length=100)
	is_active=models.BooleanField(default=True)
	is_admin=models.BooleanField(default=False)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)

	objects=UserManager()

	USERNAME_FIELD="email"
	REQUIRED_FIELDS=['name']

	def __str__(self):
		return self.name

	def has_perm(self,perm,obj=None):
		"Does User has a specific permission"
		return self.is_admin

	def has_module_perms(self,app_label):
		"Does the user has the permission to view the app `app_label` ?"
		return True  

	@property
	def is_staff(self):
		"Is user a member of staff"
		return self.is_admin
	



class Events(models.Model):
	name=models.CharField(max_length=500)
	location=models.CharField(max_length=100)
	evedate= models.DateField()
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

	def no_of_likes(self):
		return self.likers.count()

	def no_of_interested_count(self):
		return self.interested.count()

	def __str__(self):
		return self.name

	def avgrating(self):
		ratings=Rating.objects.filter(event=self)
		count = len(ratings)
		sum = 0
		for rvw in ratings:
			sum += rvw.rating
		if sum == 0:
			return 0
		s=sum/count
		return round(s,1)


	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)
		
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

		if not self.slug:
			self.slug=slugify(self.name+"-"+str(self.evedate))
		return super().save(*args,**kwargs)




class Rating(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	event=models.ForeignKey(Events,on_delete=models.CASCADE)
	rating=models.IntegerField(validators=[MaxValueValidator(5)])

	def __str__(self):
		return self.user.name


class Profile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	image=models.ImageField(upload_to="profile_pics",default="defaultProfile.jpeg")

	def __str__(self):
		return self.user.name  

	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)

		image=Image.open(self.image.path)

		if image.width > 300 or image.height > 300:
			output=(300,300)
			image.thumbnail(output)
			image.save(self.image.path)



