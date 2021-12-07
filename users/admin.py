from django.contrib import admin

# Register your models here.
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
  list_display = ('id','user','profile_picture_link','is_verified')
  search_field = ['user']


admin.site.register(CustomUser,CustomUserAdmin)
