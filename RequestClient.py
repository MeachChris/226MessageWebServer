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

#
# #PURPOSE: ASYNCHRONOUS
# #To send a command and a message to the server in a single message
# #
# #ARGUMENTS:
# #CMD - Command to send. Will be GET or PUT
# #key - Message to send. Includes alphanumeric keys of next message and previous message
# #
# def sendMessage(CMD, key):
#     if CMD == 'GET':
#         try:
#             r = requests.get('http://' + str(HOST) + ':' + str(PORT) + '/msgserver/get/' + str(key) + '/')
#             #print('The r is:  ' + str(r.content))
#             if (len(r.content) < 161):
#                 return r.content.decode('utf-8')
#             else:
#                 return "\n"
#         except ObjectDoesNotExist as DoesNotExist:
#             print('\n')
#             return "\n"

#     if CMD == 'PUT':
#         client = requests.session()
#         #print(key + " : is the full key")
#         url = 'http://' + str(HOST) + ':' + str(PORT) + '/msgserver/create/'
#         client.get(url)
#         message = key[16:] 
#         #print(message + " : is the message")
#         key = key[8:16]
#         newkey = key[:8]
#         print("key = " + key + " newkey = " + newkey + " message = " + message)
#         if 'csrftoken' in client.cookies:
#             payload = { "key": key, "message": newkey + message, 'csrfmiddlewaretoken': client.cookies['csrftoken']}
#         r = client.post(url, data = payload, headers = {'Referer' : url})
        

# def client(host, port, key):
#     data = key
#     while(data != "\n" or len(data) > 160): 
#         key = data[0:8] 
#         data = sendMessage(GET_CMD, key)
#         print(data)
#     if (len(key < 8)):

#     messageToSend = str(input("Enter your message to send: "))
#     x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
#     messageToSend = key + x + messageToSend
#     sendMessage(PUT_CMD, messageToSend)
#     #nextkey is for next message and can be assigned with x

# #Check for correct amount of arguments    
# if (len(sys.argv) != 4):
#     print(f'{sys.argv[0]} needs 3 arguments to transmit')
#     sys.exit(-1)

# client(HOST, PORT, KEY)


# client = requests.session()
#     url = 'http://' + str(HOST) + ':' + str(PORT) + '/msgserver/create/'
#     client.get(url)
######################CLIENT######################
#response is the decoded version of the data variable.  The data variable is the encoded version of the message.
#newkey is for the random key which is generated for subsequent put commands beyond the initial CLI arguement key.
#the client opens a connection for the reader/writer by using asyncio_open_connection and takes an IP and port which is a command
#line arguement, respectively IP = 1, PORT = 2.  The key is then passed by 3.
#the program will send a GET command to a server, if a response is found, it continues to ask for a put until such a time as there is no message at key.
#The dictionary at the server will be populated by this methodology and return the key/value string pairs belonging to the dictionary.

def client(HOST, PORT, KEY):
    r = requests.get('http://' + str(HOST) + ':' + str(PORT) + '/msgserver/get/' + str(KEY) + '/')
    msg = r.content.decode('utf-8')
    print("msg at top is: " + msg + "\n")         
    newkey = msg[:8]
    currentkey = KEY
    print('Received: ' + msg)
    response = msg

    while len(response) > 1:
        currentkey = response[10:18]
        r = requests.get('http://' + str(HOST) + ':' + str(PORT) + '/msgserver/get/' + str(currentkey) + '/')
        response = r.content.decode('utf-8')
        print("response in while loop is:  " +  response)


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
