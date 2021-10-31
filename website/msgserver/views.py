from django.shortcuts import render
from .models import Message
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponse
import json
from django.core.exceptions import ObjectDoesNotExist
#This gets the message from an url /get/<8digitkey> if the key is found, which must be 8 digit alphanumeric.
def getmessage(request, key):
    themessage = Message.objects.filter(key=key)
    return HttpResponse(themessage)

    #This class is a view for creation of messages.  it allows users to create messages that have not previously been used.
    #The keys must be 8 digit alphanumeric and unique.  The message must be 1 character or longer. /create/
class Createmessage(CreateView):
    model = Message
    fields = ['key', 'message']
    success_url = reverse_lazy('create')

#This class is a view for the intent of updating the view and changing a KWARG passed in the URL for the website in the form of
# an 8 digit alphenumeric key.  If it is found, message box will apear and allow the user to update the found key. /update/<key>
class UpdateMessage(UpdateView):
        model = Message
        fields = ['message']
        success_url = reverse_lazy('returnall')
        #request = ''
        def get_object(self):
        
            ToBeReturned = Message.objects.get(key=self.kwargs.get("key"))
        #stringMe = self.request
        #stringMe = str(stringMe)
        #return Message.objects.filter(key=stringMe[EXTRACT_STRING_FROM_START:EXTRACT_STRING_FROM_END])[0]
            return ToBeReturned
            

                
#This returns all of the messages from the server in the form of JSON at the default URL.
def returnall(request):
        themessages = Message.objects.all()
        returnMe = ''
        for i in themessages:
            returnMe += json.dumps(i, cls=MessageEncode) + ", "
        return HttpResponse(returnMe)
#Encodes messages in to a JSON format.
class MessageEncode(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return { 'key' : obj.key, 'message' : obj.message }
        return json.JSONEncoder.default(self, obj)



