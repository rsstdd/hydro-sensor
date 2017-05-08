#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import os
import sys
sys.path.append(os.path.join("./sources"))

from pymongo import MongoClient
from socket import gethostname
import datetime
import json
import requests


def dispatch_sensor_data(jsonPackage):
    timestamp = str(datetime.datetime.now())
    client = MongoClient('10.9.0.1')
    db = client.solstice
    collection = db[type]
    filename = "/var/local/thoth.id"
    deviceData={}
    deviceData['room']="Undefined"
    deviceData['role']="Undefined"

    try:
        with open(filename, 'r') as file:
            deviceData.json.load(file)
            file.close()
    except Exception as e:
        print e

    jsonPackage['room'] = deviceData['room']
    jsonPackage['role'] = deviceData['role']
    jsonPackage['type'] = jsonPackage['type']
    jsonPackage["timestamp"] = timestamp
    jsonPackage["sensor_version"] = "1.00"
    jsonPackage["sensor_group"] = "Production"

    sensorRecord = {"sensordata": jsonPackage}

    print sensorRecord

    try:
        record_id2 = db.sensordata.insert_one(sensorRecord)
    except:
        with open('~thoth/sensordata.txt', 'w') as outfile:
            json.dump(jsonPackage, outfile)

    # print sensorRecord

    #send to heroku

    if deviceData['room'] in ['0804', '0808']:  # skagit?
        # postAPI('https://skagit-luna-api.herokuapp.com/sensordata', jsonPackage)
        # print deviceData
    else:
        # postAPI('https://luna-api.herokuapp.com/sensordata', jsonPackage)
        # postAPI('https://luna-api-staging.herokuapp.com/sensordata', jsonPackage)

    #send to mongo

    try:
        # collection.insert_one(jsonPackage).inserted_id
        client.close()
        print "mongo sent"
    except Exception as e:
        print "hydro sensor_worker.py FAILED to send to mongo", e
        try:
            with open('sensordata.txt','a') as outfile:
                json.dump(jsonPackage, outfile)
        except:
            pass
