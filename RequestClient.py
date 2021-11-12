import requests
from django.core.exceptions import ObjectDoesNotExist
import json

#!/usr/bin/env python3

import sys, random, string

GET_CMD = "GET"
PUT_CMD = "PUT"

HOST = sys.argv[1] 
KEY = sys.argv[3]
try:
    PORT = int(sys.argv[2])
except ValueError:
    print("enter an int for port")
    sys.exit(-1)

# THIS CLIENT will take a HOST(IP), PORT, and KEY in that order in the command line.  From there it will find a message and ask you for a message.
#It will randomly generate a key, and chain the messages so that you can reach the end and input a new message with a new unique key.

#THIS FIRST GETS THE ORIGINAL KEY AND SETS VALUES FOR THE GET PORTION OR RETURNS BLANK AND GOES TO PUT PORTION.
def client(HOST, PORT, KEY):
    r = requests.get('http://' + str(HOST) + ':' + str(PORT) + '/msgserver/get/' + str(KEY) + '/')
    msg = r.content.decode('utf-8')
    print("msg at top is: " + msg + "\n")         
    newkey = msg[:8]
    currentkey = KEY
    print('Received: ' + msg)
    response = msg
# PORTION THAT IS FOR GETTING THE MESSAGE CHAIN
    while len(response) > 1:
        currentkey = response[10:18]
        r = requests.get('http://' + str(HOST) + ':' + str(PORT) + '/msgserver/get/' + str(currentkey) + '/')
        response = r.content.decode('utf-8')
        print("response in while loop is:  " +  response)
#PUT PORTION, THIS PUTS THE NEW MESSAGE WITH ITS NEW RANDOM KEY AS THE FIRST 8 CHARS OF THE MESSAGE.
    random_key = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    newMessage = random_key + input("please enter a message: \n")
    newkey = newMessage[:8]
    client = requests.session()
    url = 'http://' + str(HOST) + ':' + str(PORT) + '/msgserver/create/'
    client.get(url)
    print("key = " + currentkey + " newkey = " + random_key + " message = " + newMessage[8:])
    if 'csrftoken' in client.cookies:
        payload = { "key": currentkey, "message": newMessage, 'csrfmiddlewaretoken': client.cookies['csrftoken']}
    r = client.post(url, data = payload, headers = {'Referer' : url})
    data = r.content.decode("utf-8")

#ensures there are sufficient amount of arguements from the command line to transmit.
if len(sys.argv) != 4:
    print(f'{sys.argv[0]} needs ip, port, key arg to transmit')
    sys.exit(-1)

#runs client.
client(sys.argv[1], sys.argv[2], sys.argv[3])
