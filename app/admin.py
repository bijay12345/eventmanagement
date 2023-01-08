from django.contrib import admin
from app.models import User,Rating,Events,Profile  
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):

	list_display=("id","email","name","is_admin")
	list_filter = ("is_admin",)

	fieldsets=(
		("User Credential",{"fields":("email","password")}),
		("Personal Info",{"fields":("name",)}),
		("permissions",{"fields":("is_admin",)}),
		)

	add_fieldsets = (
			(None,{
				"classes":("wide",),
				"fields":("email","name","password1","password2"),
				}),
		)
	search_fields = ("name","id")
	ordering = ("name","id")
	filter_horizontal=()


admin.site.register(User,UserModelAdmin)

@admin.register(Events)
class EventAdmin(admin.ModelAdmin):
	list_display=['id','name','location','evedate']

admin.site.register(Rating)
admin.site.register(Profile)