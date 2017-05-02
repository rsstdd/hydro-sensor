#!/usr/bin/python
# -*- coding: utf-8 -*-

# import yocto_data
import hydro_data
from socket import gethostname
from datetime import timedelta, date
# from pymongo import MongoClient
import json
import requests

import os
import sys
sys.path.append(os.path.join("..", "..", "Sources"))

data = hydro_data.format_data()
print data


# def sensor_data_dispatch(type, jsonPackage):
#     client = MongoClient('10.9.0.1')
#     db = client.solstice
#     collection = db[type]
#
#     filename = "/var/local/thoth.id"
#
#     with open(filename, 'r') as file:
#         deviceData = json.load(file)
#         file.close()
#
#     client = MongoClient('10.9.0.1')
#     db = client.solstice
#     collection = db[type]
#     jsonPackage['type'] = type
#     jsonPackage['room'] = deviceData['room']
#     jsonPackage['role'] = deviceData['role']
#     sensorRecord = {"sensordata": jsonPackage}
#
#     print sensorRecord
#
#     try:
#         record_id2 = db.sensordata.insert_one(sensorRecord)
#     except:
#         with open('~thoth/sensordata.txt', 'w') as outfile:
#             json.dump(jsonPackage, outfile)
#
#     record_id = db[type].insert_one(jsonPackage).inserted_id
#
# 	print sensorRecord
#
#     # Send to DB
#     try:
#         # requests.post(
#         #     'https://luna-api.herokuapp.com/sensordata',
#         #     data=jsonPackage
#         # )
#         # requests.post(
#         #     'https://luna-api-staging.herokuapp.com/sensordata',
#         #     data=jsonPackage
#         # )
#     except Exception as e:
#         print e
