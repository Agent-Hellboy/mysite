from django.contrib.auth.models import AbstractUser
from django.db import models


class Team(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=255)


class User(AbstractUser):
    team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True)


class File(models.Model):
    title = models.CharField(max_length=255, blank=True)
    hash_val = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f" Title: {self.title} hash_val :{self.hash_val} uploaded_at {self.uploaded_at}"
