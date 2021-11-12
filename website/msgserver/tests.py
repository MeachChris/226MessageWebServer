from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from msgserver.models import *
import json


class MsgTestCase(TestCase):
    def test_createretrieve(self):
        response = self.client.post("/msgserver/create/", {'key' : '12345678', 'message' : 'hello'})
        #self.assertFormError(response, 'key', 'message', 'failed to put')
        m = Message.objects.get(key ='12345678')
        #print(m)
        self.assertEqual(m.message, 'hello')
        print("test_createretrieve PASSED")

    def test_duplicate(self):
        response = self.client.post("/msgserver/create/", {'key' : '12345678', 'message' : 'hello'})
        response = self.client.post("/msgserver/create/", {'key' : '12345678', 'message' : 'goodbye'})
        m = Message.objects.get(key ='12345678')
        self.assertEqual(m.message, 'hello')
        print("test_duplicate PASSED")

    def test_msgsize(self):
        #161 characters in test for message (over much)
        response = self.client.post("/msgserver/create/", {'key' : '12345677', 'message' : '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901'})
        try:
            m = Message.objects.get(key = '1235677')
            self.fail()
        except ObjectDoesNotExist as DoesNotExist:
            pass
        
            #Testing too few characters with key
        response = self.client.post("/msgserver/create/", {'key' : '1234567', 'message' : 'goodbye'})
        try:
            m = Message.objects.get(key = '123567')
            self.fail()
        except ObjectDoesNotExist as DoesNotExist:
            pass        

            #Testing too many characters with key
        response = self.client.post("/msgserver/create/", {'key' : '123456789', 'message' : 'hihi'})
        try:
            m = Message.objects.get(key = '12356789')
            self.fail()
        except ObjectDoesNotExist as DoesNotExist:
            pass  

            #Testing to ensure that a blank message cannot be passed.
        response = self.client.post("/msgserver/create/", {'key' : '12345678', 'message' : ''})
        try:
            m = Message.objects.get(key = '1235678')
            self.fail()
        except ObjectDoesNotExist as DoesNotExist:
            pass  

            #Testing alphanumeric keys
        response = self.client.post("/msgserver/create/", {'key' : '123!5&78', 'message' : ''})
        try:
            m = Message.objects.get(key = '123!5&78')
            self.fail()
        except ObjectDoesNotExist as DoesNotExist:
            pass  

            #Testing to ensure that it is working properly.
        response = self.client.post("/msgserver/create/", {'key' : '12345677', 'message' : 'Worked'})
        m = Message.objects.get(key ='12345677')
        self.assertEqual(m.message, 'Worked')
        print("test_msgsize PASSED")


    def test_update(self):
        response = self.client.post("/msgserver/create/", {'key' : '12345677', 'message' : 'original'})
        m = Message.objects.get(key ='12345677')
        self.assertEqual(m.message, 'original')
        response = self.client.post("/msgserver/update/12345677/", {'message' : 'new'})
        m = Message.objects.get(key ='12345677')
        self.assertEqual(m.message, 'new')
        print("test_update PASSED")


    def test_jsonget(self):
        response = self.client.post("/msgserver/create/", {'key' : '12345677', 'message' : 'json'})
        m = Message.objects.all()
        str(m).split(',')
        for msg in m:
            if (len(str(msg)) > 6):
                print(msg)
                json.loads(str(msg))
        
        m = Message.objects.get(key = '12345677')
        m = str(m)
        #print(m)
        json.loads(m)
        print("test_jsonget PASSED")
        
        

