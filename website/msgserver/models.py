from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

def validatekeydupe(value):
    for message in Message.objects.all():
        if message.key == value:
            raise ValidationError('Key is already in use', code='duplicate')

def validatealnum(value):
    if not (value.isalnum()):
        raise ValidationError('Must be alphanumeric', code="badAlnum")

class Message(models.Model):
    key = models.CharField(max_length=8, validators=[MinLengthValidator(8), validatealnum, validatekeydupe])
    message = models.CharField(max_length=160, validators=[MinLengthValidator(1)])
    
    def __str__(self):
        return 'KEY: ' + self.key + ', MESSAGE: ' + self.message


# Create your models here.
