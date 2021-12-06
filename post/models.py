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
    reports = models.IntegerField(default=0)

class Images(models.Model):
    public_id = models.TextField(default="")
    url = models.TextField(default="")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True,  related_name="urls")
