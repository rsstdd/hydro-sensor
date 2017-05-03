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
                'sensor_group': sensor['type'],
                'role': sensor['sensor_type'],
                'sensor_reading': sensor['sensor_reading']
            }

        hydrojson.extend(jsonPackage)

    print hydrojson
    return hydrojson

if hydroData is not None:
    format_data()
