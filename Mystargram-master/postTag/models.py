from django.db import models
from post.models import Post


class PostTag(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=20)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)