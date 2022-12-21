from email.policy import default
from django.db import models
from post.models import Post
from django.contrib.auth.models import User


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    text = models.TextField()
    time = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
