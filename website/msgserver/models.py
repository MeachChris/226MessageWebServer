from django.db import models

class Message(models.Model):
    key = models.CharField(max_length=8)
    message = models.CharField(max_length=256)

# Create your models here.
