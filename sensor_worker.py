#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import os

# from pymongo import MongoClient
from socket import gethostname
import datetime
import json
import requests


def dispatch_sensor_data(jsonPackage):
    timestamp = str(datetime.datetime.now())
    thoth = "/var/local/thoth.id"
    deviceData = {}
    deviceData['room'] = "Undefined"
    deviceData['role'] = "Undefined"

    try:
        with open(thoth, 'r') as file:
            deviceData = json.load(file)
            file.close()
    except Exception as e:
        print e

    # client = MongoClient('10.9.0.1')
    # db = client.solstice
    # collection = db[type]

    jsonPackage['room'] = deviceData['locaton']['room']
    jsonPackage['role'] = deviceData['device']['role']
    jsonPackage["timestamp"] = timestamp
    jsonPackage["sensor_version"] = "1.00"
    jsonPackage["sensor_group"] = "Production"
    #
    sensorRecord = {"sensordata": jsonPackage}


    print sensorRecord

    # try:
    #     record_id2 = db.sensordata.insert_one(sensorRecord)
    # except:
    #     with open('~thoth/sensordata.txt', 'w') as outfile:
    #         json.dump(jsonPackage, outfile)
    #
    # record_id=db[type].insert_one(jsonPackage).inserted_id
    #
    # print sensorRecord
    #
    # try:
    #     r = requests.post('https://luna-api.herokuapp.com/sensordata', data = jsonPackage)
    #     r2 = requests.post('https://luna-api-staging.herokuapp.com/sensordata', data = jsonPackage)
    # except Exception as e:
    #     print e
