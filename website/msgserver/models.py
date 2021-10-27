from django.db import models

class Message(models.Model):
    key = models.CharField(max_length=8)
    message = models.CharField(max_length=160)

    def __str__(self):
        return 'KEY: ' + self.key + ', MESSAGE: ' + self.message

# Create your models here.
