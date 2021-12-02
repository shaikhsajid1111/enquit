from django.contrib.auth.models import User
from django.db import models

class CustomUser(models.Model):
  id = models.IntegerField(primary_key=True)
  user = models.OneToOneField(User,on_delete=models.CASCADE)
  profile_picture_link = models.TextField()
  is_verified = models.BooleanField(default=False)




