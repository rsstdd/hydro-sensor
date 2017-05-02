#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json
from datetime import timedelta, date
from socket import gethostname
import requests
from pymongo import MongoClient
import gspread
import ftdi_hydro

hydroData=ftdi_hydro.read_sensors()

def postAPI(url, payload):
    try:
        r = requests.post(url, data = payload)
        assert r.status_code == 201, "%r %r != 201" % (r.url,r.status_code)
        print "sent", r.url
    except Exception as e:
        print "yocto-mongo.py FAILED to send to", e

def mongoize(type,jsonPackage):
#   print jsonPackage
    filename="/var/local/thoth.id"
    deviceData['room']="Undefined"
    deviceData['role']="Undefined"

    with open(filename,"r") as file:
        deviceData=json.load(file)
        file.close()

# Need to figure out how to config the DB stuff

    # client = MongoClient('10.9.0.1')
    # db=client.solstice
    # collection=db[type]
    jsonPackage['type'] = type
    jsonPackage['room'] = deviceData['room']
    jsonPackage['role']=deviceData['role']
    sensorRecord = {"sensordata":jsonPackage}
    print sensorRecord

    # try :
    #     # record_id2=db.sensordata.insert_one(sensorRecord)
    # except:
    #     with open('~thoth/sensordata.txt','w') as outfile:
    #         json.dump(jsonPackage, outfile)
    #
    # record_id=db[type].insert_one(jsonPackage).inserted_id

    print record_id
    print record_id2
	print sensorRecord

    #send to heroku

    # try:

        # r = requests.post('https://luna-api.herokuapp.com/sensordata', data = jsonPackage)
        # r2 = requests.post('https://luna-api-staging.herokuapp.com/sensordata', data = jsonPackage)
    # except Exception as e:
    #     print e

if hydroData is not None:
    # timestamp = datetime.datetime.now()

    for data in hydroData:
        if any('hydro-ec' in x for x in data)
            jsonPackage={
            'sensor_num': data['serial_number'],
            'hostname' : gethostname(),
            'timestamp': 'now',
            'sensor_version':'1.00',
            'sensor_group': data['name'],
            'role': data['sensor_type'],
            'type': data['sensor_type']
            }

            mongoize('hydro-ec', jsonPackage)

        if any('hydro-ph' in x for x in data)
            jsonPackage={
            'sensor_num': data['serial_number'],
            'hostname' : gethostname(),
            'timestamp': 'now',
            'sensor_version':'1.00',
            'sensor_group': data['name'],
            'role': data['sensor_type'],
            'type': data['sensor_type']
            }

            mongoize('hydro-ph', jsonPackage)

        if any('hydro-temp' in x for x in data)
            jsonPackage={
            'sensor_num': data['serial_number'],
            'hostname' : gethostname(),
            'timestamp': 'now',
            'sensor_version':'1.00',
            'sensor_group': data['name'],
            'role': data['sensor_type'],
            'type': data['sensor_type']
            }

            mongoize('hydro-temp', jsonPackage)

        if any('hydro-flow' in x for x in data)
            jsonPackage={
            'sensor_num': data['serial_number'],
            'hostname' : gethostname(),
            'timestamp': 'now',
            'sensor_version':'1.00',
            'sensor_group': data['name'],
            'role': data['sensor_type'],
            'type': data['sensor_type']
            }

            mongoize('hydro-flow', jsonPackage)

        print ''
        print jsonPackage
        print '---------------------------'
        print ''

    print '---------------------------'
    print hydroData[0]['sensor_type']
    print hydroData[0]['serial_number']
    print hydroData[0]['name']
    print hydroData[0]['sensor_reading']
    print '---------------------------'
    print hydroData[1]['sensor_type']
    print hydroData[1]['serial_number']
    print hydroData[1]['name']
    print hydroData[1]['sensor_reading']
    print '---------------------------'
    print hydroData[2]['sensor_type']
    print hydroData[2]['serial_number']
    print hydroData[2]['name']
    print hydroData[2]['sensor_reading']
    print '---------------------------'
else:
    print "None error"
