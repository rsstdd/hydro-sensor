#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import os

from socket import gethostname
import datetime
import json
import requests
from pymongo import MongoClient

thoth2 = '/var/local/thoth2.id'
thoth = '/var/local/thoth.id'


def open_thoth_id():
	"""
		Opens Thoth/Thoth2.id & returns open_thoth variable and thoth/thoth2
	"""

	thoth_data = {}
	open_thoth = ''

	if os.path.isfile(thoth2):
		open_thoth = thoth2
	elif os.path.isfile(thoth):
		open_thoth = thoth
	else:
		open_thoth = None

	thoth_data['open_thoth'] = open_thoth

	try:
		with open(open_thoth) as file:
			thoth_data['deviceData'] = json.load(file)
			file.close()
	except Exception as e:
		print e

	return thoth_data


def postAPI(url, payload):
	try:
		r = requests.post(url, data=payload)
		assert r.status_code == 201, "%r %r != 201" % (r.url, r.status_code)
		print 'sent', r.url
	except Exception as e:
		print 'sensor-worker.py FAILED to send to', e
		print ''


def send_to_mongo(payload, sensor_type):
	try:
		client = MongoClient('10.9.0.1')
		db = client.solstice
		collection = db[sensor_type]
		record_id2 = db.sensordata.insert_one(payload)
		client.close()
		print 'mongo sent'
	except Exception as e:
		print 'sensor-worker.py FAILED to send to mongo', e

		try:
			with open('/home/pi/sensordata.txt', 'a') as outfile:
				json.dump(payload, outfile)
		except:
			pass


def format_sensor_data(dataPackage):
	"""
		Wraps sensor data with device/thoth metadata;
		Returns a dict of formatted data and the customerName
	"""

	thoth_information = open_thoth_id()

	deviceData = thoth_information['deviceData']
	open_thoth = thoth_information['open_thoth']

	formatted_sensor_data = {}
	room = ''
	role = ''
	hostname = ''
	sensor_type = ''
	customerName = ''

	dataPackage['timestamp'] = datetime.datetime.utcnow()
	dataPackage['net_hostname'] = gethostname()

	if open_thoth == thoth2:
		formatted_sensor_data['customerName'] = deviceData['customer']['customerName']
		sensor_type = deviceData['device']['role']

		dataPackage['room'] = deviceData['location']['room']
		dataPackage['role'] = deviceData['device']['role']
		dataPackage['hostname'] = deviceData['device']['hostname']
		dataPackage['sensor_version'] = deviceData['device']['sensorVersion']
	elif open_thoth == thoth:
		dataPackage['room'] = deviceData['room']
		dataPackage['role'] = deviceData['role']
		dataPackage['hostname'] = deviceData['hostname']
		dataPackage['sensor_group'] = 'Test'
		sensor_type = deviceData['role']
		formatted_sensor_data['customerName'] = customerName
	else:
		dataPackage['room'] = room
		dataPackage['role'] = role
		dataPackage['hostname'] = hostname
		dataPackage['sensor_group'] = 'Test'
		dataPackage['sensor_type'] = sensor_type
		formatted_sensor_data['customerName'] = customerName

	formatted_sensor_data['dataPackage'] = dataPackage

	print 'formatted_sensor_data: ', formatted_sensor_data
	return formatted_sensor_data


def dispatch_sensor_data(dataPackage):
	"""
		Determines where to send Sensor Data & posts to API and Mongo
	"""

	formatted_data_sensor = format_sensor_data(dataPackage)

	dataPackage = formatted_sensor_data['dataPackage']
	customerName = formatted_sensor_data['customerName']
	sensor_type = dataPackage['type']

	print dataPackage
	print ''

	sensorRecord = {'sensordata': dataPackage}

	# Send to heroku
	if customerName.lower() == 'skagit' or 'room' in dataPackage and dataPackage['room'] in ['0804', '0808']:
		postAPI('https://skagit-luna-api.herokuapp.com/sensordata', dataPackage)
	else:
		postAPI('https://luna-api.herokuapp.com/sensordata', dataPackage)
		postAPI('https://luna-api-staging.herokuapp.com/sensordata', dataPackage)

	#  Send to Mongo
	send_to_mongo(sensorRecord, sensor_type)
