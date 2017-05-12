#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import os

from socket import gethostname
import datetime
import json
import requests


def postAPI(url, payload):
    try:
        r = requests.post(url, data=payload)
        assert r.status_code == 201, "%r %r != 201" % (r.url, r.status_code)
        print "sent", r.url
    except Exception as e:
        print "sensor-worker.py FAILED to send to", e


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

    jsonPackage['room'] = deviceData['locaton']['room']
    jsonPackage['role'] = deviceData['device']['role']
    jsonPackage["timestamp"] = timestamp
    jsonPackage["sensor_version"] = "1.00"
    jsonPackage["sensor_group"] = "test"

    sensorRecord = {"sensordata": jsonPackage}

    try:
        print jsonPackage
        # postAPI('https://luna-api.herokuapp.com/sensordata', jsonPackage)
        # postAPI('https://luna-api-staging.herokuapp.com/sensordata', jsonPackage)
    except:
        with open('~thoth/sensordata.txt', 'w') as outfile:
            json.dump(jsonPackage, outfile)
