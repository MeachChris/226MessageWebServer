from django.shortcuts import render
from .models import Message
from django.http import HttpResponse

def getmessage(request, key):
    messagetoget = Message.objects.filter(key=key)
    return HttpResponse(messagetoget)

