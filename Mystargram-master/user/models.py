from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=20)
    pw = models.CharField(max_length=64)
    intro = models.CharField(max_length=100)
    userpic = models.CharField(max_length=100)
    favorite=models.CharField(max_length=100, default=0)
