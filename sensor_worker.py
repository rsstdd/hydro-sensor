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
        print ''
        print "sensor-worker.py FAILED to send to", e
        print ''


def dispatch_sensor_data(dataPackage):
    timestamp = str(datetime.datetime.now())
    thoth = "/var/local/thoth.id"
    deviceData = {}
    deviceData['room'] = 'undefined'
    deviceData['role'] = 'undefined'

    try:
        with open(thoth, 'r') as file:
            deviceData = json.load(file)
            file.close()
    except Exception as e:
        print e

    dataPackage['type'] = deviceData['device']['hostname']
    dataPackage['room'] = deviceData['location']['room']
    dataPackage['role'] = deviceData['device']['deviceRole']
    dataPackage["timestamp"] = timestamp
    dataPackage["sensor_group"] = "test"
    dataPackage["sensor_version"] = "1.00"

    sensorRecord = {"sensordata": dataPackage}
    jsonPackage = json.dumps(sensorRecord)

    print jsonPackage
    print ''

    # Heroku
    # try:
    #     postAPI('http://localhost:4000/sensordata', dataPackage)
    #     print ''
    # except:
    #     with open('~thoth/sensordata.txt', 'w') as outfile:
    #         json.dump(jsonPackage, outfile)
    # #
    # # Mongo
    # try:
    #     client = MongoClient('10.9.0.1:27017')
    #     db = client.solstice
    #     collection = db[type]
    #     record_id2 = db.sensordata.insert_one(sensorRecord)
    #     client.close()
    #     print "mongo sent"
    #
    # except Exception as e:
    #     print "sensor-worker.py FAILED to send to mongo", e
    #
    #     try:
    #         with open('sensordata.txt','a') as outfile:
    #             json.dump(jsonPackage, outfile)
    #     except:
    #         pass
