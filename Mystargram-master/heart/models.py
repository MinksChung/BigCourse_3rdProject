from django.db import models

from post.models import Post
from user.models import User


class Heart(models.Model):
        id = models.AutoField(primary_key=True)
        post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
        user_id = models.ForeignKey(User, on_delete=models.CASCADE)