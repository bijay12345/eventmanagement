from django.contrib import admin
from app.models import Rating,Events,Comment,Article,WorkingModel,Mission


admin.site.register(Events)

admin.site.register(Rating)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display=['id','event','user','date_commented']

@admin.register(Article)
class CommentAdmin(admin.ModelAdmin):
	list_display=['id','heading']

@admin.register(WorkingModel)
class CommentAdmin(admin.ModelAdmin):
	list_display=['id','heading']

@admin.register(Mission)
class CommentAdmin(admin.ModelAdmin):
	list_display=['id','heading']