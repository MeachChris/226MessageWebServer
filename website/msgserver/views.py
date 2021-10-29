from django.shortcuts import render
from .models import Message
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponse
import json

def getmessage(request, key):
    themessage = Message.objects.filter(key=key)
    return HttpResponse(themessage)

    
class Createmessage(CreateView):
    model = Message
    fields = ['key', 'message']
    success_url = reverse_lazy('create')


class UpdateMessage(UpdateView):
    
    model = Message
    fields = ['message']
    
    success_url = reverse_lazy('returnall')
    def get_object(self):
        #stringMe = self.request
        #stringMe = str(stringMe)
        #return Message.objects.filter(key=stringMe[EXTRACT_STRING_FROM_START:EXTRACT_STRING_FROM_END])[0]
        return Message.objects.get(key=self.kwargs.get("key"))
        
def returnall(request):
        themessages = Message.objects.all()
        returnMe = ''
        for i in themessages:
            returnMe += json.dumps(i, cls=MessageEncode) + ", "
        return HttpResponse(returnMe)

class MessageEncode(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return { 'key' : obj.key, 'message' : obj.message }
        return json.JSONEncoder.default(self, obj)



