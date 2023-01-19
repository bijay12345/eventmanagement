from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField

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


class Host(AbstractBaseUser):
	email=models.EmailField(verbose_name="Email Address",max_length=255,unique=True)
	name=models.CharField(max_length=100)
	is_active=models.BooleanField(default=True)
	is_admin=models.BooleanField(default=False)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)


	objects=UserManager()

	USERNAME_FIELD="email"
	REQUIRED_FIELDS=["name"]

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



	

class Profile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	image=models.ImageField(upload_to="profile_pics",default="defaultProfile.jpeg")
	phonenumber = PhoneNumberField(blank=True)
	location=models.CharField(max_length=50,blank=True)
	bio=models.CharField(max_length=100,blank=True)

	def __str__(self):
		return self.user.name  

	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)

		image=Image.open(self.image.path)

		if image.width > 300 or image.height > 300:
			output=(300,300)
			image.thumbnail(output)
			image.save(self.image.path)




