#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json
from datetime import timedelta, date
from socket import gethostname
import requests
import ftdi_hydro

hydroData=ftdi_hydro.read_sensors()

if hydroData is not None:
    # timestamp = datetime.datetime.now()

    for data in hydroData:
        print data['name']
        if data['name'] == 'hydro-ec':
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

        if data['name'] == 'hydro-ph':
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

        if data['name'] == 'hydro-temp':
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

        if data['name'] == 'hydro-flow':
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


#         print ''
#         print jsonPackage
#         print '---------------------------'
#         print ''
#
#     print '---------------------------'
#     print hydroData[0]['sensor_type']
#     print hydroData[0]['serial_number']
#     print hydroData[0]['name']
#     print hydroData[0]['sensor_reading']
#     print '---------------------------'
#     print hydroData[1]['sensor_type']
#     print hydroData[1]['serial_number']
#     print hydroData[1]['name']
#     print hydroData[1]['sensor_reading']
#     print '---------------------------'
#     print hydroData[2]['sensor_type']
#     print hydroData[2]['serial_number']
#     print hydroData[2]['name']
#     print hydroData[2]['sensor_reading']
#     print '---------------------------'
# else:
#     print "None error"
