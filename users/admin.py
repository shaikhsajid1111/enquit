from django.contrib import admin

# Register your models here.
from .models import CustomUser, ReportAccount

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'profile_picture_link',
                    'is_verified', 'report_count')
    search_field = ['user']


admin.site.register(CustomUser, CustomUserAdmin)


class ReportAccountAdmin(admin.ModelAdmin):
    list_display = ['get_username']

admin.site.register(ReportAccount,ReportAccountAdmin)