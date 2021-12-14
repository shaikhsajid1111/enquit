from django.contrib import admin

# Register your models here.
from .models import Post,Images,Vote,Report,Answer
class PostAdmin(admin.ModelAdmin):
  list_display = ('post_id','author','posted_on','text')
  search_field = ['text','author']


admin.site.register(Post,PostAdmin)


class ImageAdmin(admin.ModelAdmin):
  list_display = ('public_id', 'url', 'post')
  search_field = ['text', 'author']

admin.site.register(Images,ImageAdmin)


class VoteAdmin(admin.ModelAdmin):
  list_display = ('user', 'post', 'created')
  search_field = ['user', 'post']


admin.site.register(Vote,VoteAdmin)

class ReportAdmin(admin.ModelAdmin):
  list_display = ('user', 'post', 'created')
  search_field = ['user', 'post']


admin.site.register(Report,ReportAdmin)
admin.site.register(Answer)