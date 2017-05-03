#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from datetime import timedelta, date
import os, sys
# add ../sources to the PYTHONPATH
sys.path.append(os.path.join('./sources'))
import atlas_hydro

hydroData = atlas_hydro.get_sensor_data()
print atlas_hydro.get_sensor_data()

def format_data():
    hydrojson = []

    if hydroData is not None:
        for sensor in hydroData:
            print sensor
            jsonPackage = {
                'sensor_num': sensor['serial_number'],
                'timestamp': 'Should-be-timestamp',
                'sensor_version': '1.00',
                'sensor_group': 'Production'
                'role': sensor['sensor_type'],
                sensor['type']: sensor['sensor_reading']
            }

        hydrojson.append(jsonPackage)

    print hydrojson
    print '----'
    # return hydrojson

if hydroData is not None:
    format_data()
