from django.db import models
from users.models import CustomUser
from django.utils.timezone import now

class Post(models.Model):
  post_id = models.IntegerField(primary_key=True)
  author = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=False)
  text =models.TextField(default="")
  posted_on = models.DateTimeField(default=now,editable=False)
  reports = models.IntegerField()

