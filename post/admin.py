from django.contrib import admin
# Register your models here.
from .models import Post, Medias, Vote, Post_Report, Answer, ReportOfAnswer
class PostAdmin(admin.ModelAdmin):
  list_display = ('post_id', 'username', 'posted_on', 'text', 'report_count')
  search_field = ['text','author']


admin.site.register(Post,PostAdmin)


class MediasAdmin(admin.ModelAdmin):
  list_display = ('public_id', 'url', 'post')
  search_field = ['text', 'author']

admin.site.register(Medias,MediasAdmin)


class VoteAdmin(admin.ModelAdmin):
  list_display = ('username', 'get_post_id', 'created')
  search_field = ['user', 'post']


admin.site.register(Vote,VoteAdmin)

class ReportAdmin(admin.ModelAdmin):
  list_display = ('user', 'post', 'created')
  search_field = ['user', 'post']


admin.site.register(Post_Report, ReportAdmin)

class AnswerAdmin(admin.ModelAdmin):
  list_display = ['username', 'text', 'timestamp', 'report_count']
admin.site.register(Answer,AnswerAdmin)

class ReportOfAnswerAdmin(admin.ModelAdmin):
  list_display = ('answer', 'created',)


admin.site.register(ReportOfAnswer,ReportOfAnswerAdmin)