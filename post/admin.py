from django.contrib import admin

# Register your models here.
from .models import Post,Images


admin.site.register(Post)
admin.site.register(Images)