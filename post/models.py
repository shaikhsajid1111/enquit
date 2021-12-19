from django.db import models
from users.models import CustomUser
from django.utils.timezone import now

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=False)
    text = models.TextField(default="")
    posted_on = models.DateTimeField(default=now, editable=False)
    report_count = models.IntegerField(default=0)
    def username(self):
      return self.author.user.username

    class Meta:
        ordering = ['-posted_on']


class Medias(models.Model):
    public_id = models.TextField(default="")
    url = models.TextField(default="")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True,  related_name="urls")


class Vote(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             null=True,  related_name="vote")
    created = models.DateTimeField(default=now, editable=False)

    def get_post_id(self):
      return self.post.post_id

    def username(self):
      return self.user.user

class Post_Report(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             null=True,  related_name="report")
    created = models.DateTimeField(default=now, editable=False)


class Answer(models.Model):
    text = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)
    report_count = models.IntegerField(default=0)
    def username(self):
      return self.user.user

class ReportOfAnswer(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=False)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE,
                              null=True,  related_name="answer_report")
    created = models.DateTimeField(default=now, editable=False)

class Answer_Vote(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=False)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE,
                               null=True,  related_name="answer_vote")
    created = models.DateTimeField(default=now, editable=False)


class Vault(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=now, editable=False)

class Tags(models.Model):
  text = models.CharField(max_length=200,default="")
  tag = models.ForeignKey(Post,on_delete=models.CASCADE)