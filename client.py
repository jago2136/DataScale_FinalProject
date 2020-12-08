#!/usr/bin/env python3
import requests
import json
import sys
import jsonpickle


def putTrackInfo(host_addr, tracknum):
	headers= {'content-type':'application/json'}
	url=host_addr+'/track'
	number=jsonpickle.encode({"number":tracknum})
	response=requests.post(url, data=number, headers=headers)
	print("Response is", response)
	print(json.loads(response.text))

def getHompage(host_addr):
	headers= {'content-type':'application/json'}
	url=host_addr+'/getInfoHomepage'
	response=requests.get(url, headers=headers)
	print("Response is", response)
	print(json.loads(response.text))

host=sys.argv[1]
addr="http://"+host+":5000"
command=sys.argv[2]
tracking_num=sys.argv[3]

if command=='track':
	putTrackInfo(addr,tracking_num)
elif command=='getInfo':
	getHomepage(addr)
else:
	print("Command not recognized")
