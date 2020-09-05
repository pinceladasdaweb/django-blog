from django.db import models
from posts.models import Post
from django.utils import timezone
from django.contrib.auth.models import User


class Comment(models.Model):
    author = models.CharField(max_length=150)
    email = models.EmailField()
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.author
