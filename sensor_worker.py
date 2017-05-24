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
		assert r.status_code == 201, "%r %r != 201" % (r.url, r.status_code)
		print "sent", r.url
	except Exception as e:
		print "sensor-worker.py FAILED to send to", e
		print ''


def dispatch_sensor_data(dataPackage):
	timestamp = str(datetime.datetime.now())
	thoth = "/var/local/thoth.id"

	try:
		with open(thoth, 'r') as file:
			deviceData = json.load(file)
			file.close()
	except Exception as e:
		print e

	# print deviceData

	sensor_type = deviceData['device']['deviceRole']
	dataPackage['hostname'] = deviceData['device']['hostname']
	dataPackage['title'] = deviceData['device']['deviceRole']
	dataPackage['room'] = deviceData['location']['room']
	dataPackage['role'] = deviceData['device']['deviceRole']
	dataPackage["sensor_group"] = "test"
	dataPackage["sensor_version"] = "1.00"
	dataPackage["timestamp"] = timestamp

	sensorRecord = {}
	sensorRecord = {"sensordata": dataPackage}

	print sensorRecord
	print ''


	#  Heroku

	# if Skagit
	if deviceData['location']['room'] in ['0804', '0808']:
		postAPI('https://skagit-luna-api.herokuapp.com/sensordata', sensorRecord)
	else:
		postAPI('https://luna-api.herokuapp.com/sensordata', sensorRecord)
		postAPI('https://luna-api-staging.herokuapp.com/sensordata', sensorRecord)


	#  Mongo
	try:
		client = MongoClient('10.9.0.1')
		db=client.solstice
		collection = db[sensor_type]
		record_id2 = db.sensordata.insert_one(sensorRecord)
		client.close()
		print "mongo sent"
	except Exception as e:
		print "sensor-worker.py FAILED to send to mongo", e

		try:
			with open('/home/pi/sensordata.txt','a') as outfile:
				json.dump(jsonPackage, outfile)
		except:
			pass
