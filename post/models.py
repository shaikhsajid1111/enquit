from django.db import models
from users.models import CustomUser
from django.utils.timezone import now
from cloudinary.models import CloudinaryField


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=False)
    text = models.TextField(default="")
    posted_on = models.DateTimeField(default=now, editable=False)
    class Meta:
      ordering = ['-posted_on']

class Images(models.Model):
    public_id = models.TextField(default="")
    url = models.TextField(default="")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True,  related_name="urls")


class Vote(models.Model):
  user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=False)
  post = models.ForeignKey(Post, on_delete=models.CASCADE,
                           null=True,  related_name="vote")
  created = models.DateTimeField(default=now, editable=False)

class Report(models.Model):
  user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=False)
  post = models.ForeignKey(Post, on_delete=models.CASCADE,
                           null=True,  related_name="report")
  created = models.DateTimeField(default=now, editable=False)



"""
class Answer(models.Model):
  post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="answer")
  author = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='author')
  text = models.TextField()
  date_created = models.DateTimeField(default=now,editable=False)
  parent = models.ForeignKey("self",null=True,blank=True,related_name="replies",on_delete=models.CASCADE)

  def __str__(self):
    return self.text
"""
