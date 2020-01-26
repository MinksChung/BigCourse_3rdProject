from django.db import models

from user.models import User


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    img1 = models.CharField(max_length=100)
    img2 = models.CharField(max_length=100)
    img3 = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
