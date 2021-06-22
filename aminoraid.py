#library in development! 
import requests
import json
import random
import base64
import string

from hashlib import sha1
from uuid import UUID

def deviceIdgenerator(st: int = 69):
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = st))
    deviceid = '01' + (MetaSpecial := sha1(ran.encode("utf-8"))).hexdigest() + sha1(bytes.fromhex('01') + MetaSpecial.digest() + base64.b64decode("6a8tf0Meh6T4x7b0XvwEt+Xw6k8=")).hexdigest()
    return deviceid

class Client():
	def __init__(self, email, password, deviceId: str=deviceIdgenerator()):
		self.api = "https://service.narvii.com/api/v1/"
		self.headers = {
		"NDCDEVICEID": deviceId,
		"NDC-MSG-SIG": "AWe7V9JF4yRIpQL1WhgoY6ZR9IXV",
		"Accept-Language": "en-US",
		"Content-Type": "application/json; charset=utf-8",
		"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-G925F Build/MMB29K.G925FXXS4DPH8; com.narvii.amino.master/3.4.33571)", 
		"Host": "service.narvii.com",
		"Accept-Encoding": "gzip",
		"Connection": "Keep-Alive"
		}
		data = {"email": email, "secret": "0 "+password, "deviceID": self.headers["NDCDEVICEID"]}
		data = json.dumps(data)
		request = requests.post(f"{self.api}g/s/auth/login", headers=self.headers, data=data)
		response = json.loads(request.text)
		print(f"Logged in {email}")
		self.sid = response['sid']
		self.userId = response['auid']
		self.deviceId = deviceId

	def get_from_url(self, url: str):
		request = requests.get(f"{self.api}/g/s/link-resolution?q={url}", headers=self.headers)
		response = json.loads(request.text)

	def send_msg(self, ndcId, threadId, message, msgType: int = 0):
   		data = {
   		"content": message,
   		"type": msgType,
   		"clientRefId": int(timestamp() / 10 % 1000000000),
   		"timestamp": (int(time.time() * 1000))
   		}
   		data = json.dumps(data)
   		request = requests.post(f"{self.api}x{ndcId}/s/chat/thread/{threadId}/message", headers=self.headers, data=data)
   		response = json.loads(request.text)
        
	def join_chat(self, ndcId, threadId):
	  	request = requests.post(f"{self.api}x{ndcId}/s/chat/thread/{threadId}/member/{self.userId}", headers=self.headers)
	  	response = json.loads(request.text)
   
	def leave_chat(self, ndcId, threadId):
	  	request = requests.delete(f"{self.api}/x{ndcId}/s/chat/thread/{threadId}/member/{self.userId}", headers=self.headers)
	  	response = json.loads(request.text)
   
	def send_typing(self, ndcId, threadId):
	           data = {
	           "o": {
	           "actions": ["Typing"],
	           "target": f"ndc://x{ndcId}/chat-thread/{threadId}",
	           "ndcId": int(ndcId),
	           "params": {"threadType": 2},
	           "id": "2713103"
	           },
	           "t": 304
	           }
	           data = json.dumps(data)
	           self.send(data)
