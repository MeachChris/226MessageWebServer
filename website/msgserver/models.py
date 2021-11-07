from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist


#This is to ensure that the key is not a duplicate that has been previously passed.
def validatekeydupe(value):
    for message in Message.objects.all():
        if message.key == value:
            raise ValidationError('Key is already in use', code='duplicate')
#This is to validate that the value passed in the key is alphanumeric.
def validatealnum(value):
    if not (value.isalnum()):
        raise ValidationError('Must be alphanumeric', code="badAlnum")


#this is the message model to define key and message pairs in the database.
class Message(models.Model):
    key = models.CharField(max_length=8, validators=[MinLengthValidator(8), validatealnum, validatekeydupe])
    message = models.CharField(max_length=160, validators=[MinLengthValidator(1)])
    #returns key/ message
    def __str__(self):
        return '{\"key\": \"' + self.key + '\", \"message\":\"' + self.message + '\"}'


# TEST CASES:::::::::::::::::::::::::::::::::::::::::::::::::

