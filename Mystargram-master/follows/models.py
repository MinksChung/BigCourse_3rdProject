from django.db import models
from user.models import User


class Follows(models.Model):
    id = models.AutoField(primary_key=True)
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followee")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
