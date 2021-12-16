from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

class CustomUser(models.Model):
  id = models.IntegerField(primary_key=True)
  user = models.OneToOneField(User,on_delete=models.CASCADE)
  profile_picture_link = models.TextField()
  is_verified = models.BooleanField(default=False)

class ReportAccount(models.Model):
  user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
  report = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
  created = models.DateTimeField(default=now, editable=False)


