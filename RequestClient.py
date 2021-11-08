import requests
from django.core.exceptions import ObjectDoesNotExist
import json
#
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
#PURPOSE: ASYNCHRONOUS
#To send a command and a message to the server in a single message
#
#ARGUMENTS:
#CMD - Command to send. Will be GET or PUT
#key - Message to send. Includes alphanumeric keys of next message and previous message
#
def sendMessage(CMD, key):
    if CMD == 'GET':
        try:
            r = requests.get('http://' + str(HOST) + ':' + str(PORT) + '/msgserver/get/' + str(key) + '/')
            #print('The r is:  ' + str(r.content))
            if (len(r.content) < 161):
                r = r.content
                return r.decode('utf-8')
            else:
                return "\n"
        except ObjectDoesNotExist as DoesNotExist:
            print('\n')
            return "\n"

    if CMD == 'PUT':
        client = requests.session()
        #print(key + " : is the full key")
        url = 'http://' + str(HOST) + ':' + str(PORT) + '/msgserver/create/'
        client.get(url)
        message = key[16:] 
        #print(message + " : is the message")
        key = key[8:16]
        if 'csrftoken' in client.cookies:
            payload = { "key": key, "message": message, 'csrfmiddlewaretoken': client.cookies['csrftoken']}
        #print(key + " : is the new key")
        
        r = client.post(url, data = payload, headers = {'Referer' : url})
        
    #reader, writer = await asyncio.open_connection(HOST,PORT)
    #message = CMD + key
    #writer.write(message.encode('utf-8') + b'\n') 
    #data = await reader.readline() 
    #writer.close() 
    #await writer.wait_closed() 
    #return data

#
#PURPOSE: ASYNCHRONOUS
#Client checks for key sent in from command line and checks against server
#to see if there is a matching key. If there is, it sends back the message associated
#with that key and goes to next key specified by the messasage.
#When no message/key is returned, user is prompted to enter their message
#Message is then saved in the server.
#
#ARGUMENTS: 
# host - IP address of server
# port - port number on server (12345)
# key - 8 digit alphanumeric key 
#
def client(host, port, key):
    data = key
    while(data != "\n" and len(data) < 10): 
        key = data[0:8] 
        data = sendMessage(GET_CMD, key)
        print(data)
    messageToSend = str(input("Enter your message to send: "))
    x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
    messageToSend = key + x + messageToSend
    sendMessage(PUT_CMD, messageToSend)
    #nextkey is for next message and can be assigned with x

#Check for correct amount of arguments    
if (len(sys.argv) != 4):
    print(f'{sys.argv[0]} needs 3 arguments to transmit')
    sys.exit(-1)

client(HOST, PORT, KEY)
