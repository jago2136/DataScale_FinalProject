#!/usr/bin/env python3
import requests
import json
import sys
import jsonpickle
import unittest

class test_build(unittest.TestCase):

	#test connection to server
	def test_1(self):
		headers= {'content-type':'application/json'}
		url='http://localhost:5000'+'/track/'+str(123)
		response=requests.get(url, headers=headers)
		res=json.loads(response)
		self.assertEqual(res['server'], 'success')
		#test a working tracking number	

if __name__ == '__main__':
	unittest.main()