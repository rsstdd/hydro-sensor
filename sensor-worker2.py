#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import os

from socket import gethostname
import datetime
import json
import requests
from pymongo import MongoClient


def postAPI(url, payload):
	try:
		r = requests.post(url, data=payload)
		assert r.status_code == 201, "%r %r != 201"%(r.url, r.status_code)
		print 'sent', r.url
	except Exception as e:
		print 'sensor-worker.py FAILED to send to', e
		print ''


def dispatch_sensor_data(dataPackage):
	timestamp = datetime.datetime.utcnow()
	thoth2 = '/var/local/thoth2.id'
	thoth = '/var/local/thoth.id'

	deviceData = {}
	deviceData['room']='Undefined'
	deviceData['role']='Undefined'

	dataPackage['sensor_group'] = 'Test'
	dataPackage['sensor_version'] = '1.00'
	dataPackage['timestamp'] = timestamp

	if os.path.isfile(thoth2):
		try:
			with open(thoth2, 'r') as file:
				deviceData = json.load(file)
				file.close()
		except Exception as e:
			print e

		dataPackage['hostname'] = deviceData['device']['hostname']
		dataPackage['room'] = deviceData['location']['room']
		dataPackage['role'] = deviceData['device']['deviceRole']
		sensor_type = deviceData['device']['deviceRole']

	else:
		try:
			with open(thoth, 'r') as file:
				deviceData = json.load(file)
				file.close()
		except Exception as e:
			print e

		dataPackage['hostname'] = deviceData['hostname']
		dataPackage['room'] = deviceData['room']
		dataPackage['role'] = deviceData['role']
		sensor_type = deviceData['role']

	sensorRecord = {}
	sensorRecord = {'sensordata': dataPackage}

	print sensorRecord
	print ''

	# Send to heroku
	customerName = deviceData['customer']['customerName']

	if customerName.lower() == 'skagit' or dataPackage['room'] in ['0804', '0808']:
		postAPI('https://skagit-luna-api.herokuapp.com/sensordata', dataPackage)
	else:
		postAPI('https://luna-api.herokuapp.com/sensordata', dataPackage)
		postAPI('https://luna-api-staging.herokuapp.com/sensordata', dataPackage)

	#  Send to Mongo
	try:
		client = MongoClient('10.9.0.1')
		db=client.solstice
		collection = db[sensor_type]
		record_id2 = db.sensordata.insert_one(sensorRecord)
		client.close()
		print 'mongo sent'
	except Exception as e:
		print 'sensor-worker.py FAILED to send to mongo', e

		try:
			with open('/home/pi/sensordata.txt', 'a') as outfile:
				json.dump(dataPackage, outfile)
		except:
			pass
