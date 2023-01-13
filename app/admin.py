from django.contrib import admin
from app.models import Rating,Events,Comment

@admin.register(Events)
class EventAdmin(admin.ModelAdmin):
	list_display=['id','name','location','evedate']

admin.site.register(Rating)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display=['id','event','user','date_commented']