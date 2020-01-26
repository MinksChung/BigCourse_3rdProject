from django.db import models
from django.utils.datetime_safe import date

from user.models import User


class Notification(models.Model):
        id = models.AutoField(primary_key=True)
        userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userid")
        fromid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fromid")
        note_type = models.IntegerField()
        seen = models.BooleanField(default=1)
        time = models.DateTimeField(auto_now_add=True)
