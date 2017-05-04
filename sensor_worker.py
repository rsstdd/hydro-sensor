#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.join("./sources"))

from pymongo import MongoClient
from socket import gethostname
from datetime import timedelta, date
import json
import requests


def dispatch_sensor_data(type, jsonPackage):
    # client = MongoClient('10.9.0.1')
    # db = client.solstice
    # collection = db[type]

    # filename = "/var/local/thoth.id"
    #
    # with open(filename, 'r') as file:
    #     deviceData = json.load(file)
    #     file.close()
    #
    # collection = db[type]
    #
    # jsonPackage['room'] = deviceData['room']
    # jsonPackage['role'] = deviceData['role']
    #
    # jsonPackage['type'] = type
    # jsonPackage["room"] = "ROOM"
    jsonPackage["timestamp"] = "Should-be-timestamp"
    jsonPackage["sensor_version"] = "1.00"
    jsonPackage["sensor_group"] = "Test"

    sensorRecord = {"sensordata": jsonPackage}

    # try:
    #     # record_id2 = db.sensordata.insert_one(sensorRecord)
    # except:
    #     with open('~thoth/sensordata.txt', 'w') as outfile:
    #         json.dump(jsonPackage, outfile)
    #
    # record_id = db[type].insert_one(jsonPackage).inserted_id

    print sensorRecord

    # # Send to DB
    # try:
    #     requests.post(
    #         'https://luna-api.herokuapp.com/sensordata',
    #         data=jsonPackage
    #     )
    #     requests.post(
    #         'https://luna-api-staging.herokuapp.com/sensordata',
    #         data=jsonPackage
    #     )
    # except Exception as e:
    #     print e
