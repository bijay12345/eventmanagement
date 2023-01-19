from django.contrib import admin
from app.models import Rating,Events,Comment


admin.site.register(Events)

admin.site.register(Rating)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display=['id','event','user','date_commented']