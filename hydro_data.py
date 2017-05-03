#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from datetime import timedelta, date
import os, sys
# add ../sources to the PYTHONPATH
sys.path.append(os.path.join('./sources'))
import atlas_hydro

hydroData = atlas_hydro.read_sensors()

def format_data():
    hydrojson = []

    if hydroData is not None:
        for sensor in hydroData:

            # jsonPackage = {
            #     'sensor_num': sensor['serial_number'],
            #     'timestamp': 'Should-be-timestamp',
            #     'sensor_version': '1.00',
            #     'sensor_group': 'Production',
            #     'role': sensor['sensor_type'],
            #     sensor['type']: sensor['sensor_reading']
            # }

        hydrojson.append({
            'sensor_num': sensor['serial_number'],
            'timestamp': 'Should-be-timestamp',
            'sensor_version': '1.00',
            'sensor_group': 'Production',
            'role': sensor['sensor_type'],
            sensor['type']: sensor['sensor_reading']
        })

    print '----'
    print hydrojson
    print ''

if hydroData is not None:
    format_data()
