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
	thoth2 = '/var/local/thoth2.id'
	thoth = '/var/local/thoth.id'
	deviceData = {}

	if os.path.isfile(thoth2):
		open_thoth = thoth2
	elif os.path.isfile(thoth):
		 open_thoth = thoth
	else:
		open_thoth = None

	try:
		with open(open_thoth) as file:
			deviceData = json.load(file)
			file.close()
	except Exception as e:
		print e

	dataPackage['timestamp'] = datetime.datetime.utcnow()
	customerName = ''

	if open_thoth == thoth2:
		customerName = deviceData['customer']['customerName']
		sensor_type = deviceData['device']['role']

		dataPackage['hostname'] = deviceData['device']['hostname']
		dataPackage['role'] = deviceData['device']['role']
		dataPackage['room'] = deviceData['location']['room']
		dataPackage['sensor_group'] = deviceData['device']['sensorGroup']
		dataPackage['sensor_version'] = deviceData['device']['sensorVersion']
	elif open_thoth == thoth:
		sensor_type = deviceData['role']

		dataPackage['hostname'] = deviceData['hostname']
		dataPackage['room'] = deviceData['room']
		dataPackage['role'] = deviceData['role']
		dataPackage['sensor_group'] = 'Production'
		dataPackage['sensor_version'] = '1.00'

	sensorRecord = {'sensordata': dataPackage}
	print sensorRecord
	print ''

	# Send to heroku
	# Skagit?
	if customerName.lower() == 'skagit' or 'room' in dataPackage and dataPackage['room'] in ['0804', '0808']:
		postAPI('https://skagit-luna-api.herokuapp.com/sensordata', dataPackage)
	else:
		postAPI('https://luna-api.herokuapp.com/sensordata', dataPackage)
		postAPI('https://luna-api-staging.herokuapp.com/sensordata', dataPackage)

	# Send to Mongo
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
			with open('/home/thoth/sensordata.txt', 'a') as outfile:
				json.dump(dataPackage, outfile)
		except:
			pass
