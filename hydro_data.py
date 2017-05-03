#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from datetime import timedelta, date
import os, sys
# add ../sources to the PYTHONPATH
sys.path.append(os.path.join('./sources'))
import atlas_hydro


def format_data():
    hydrojson = []

    hydroData = atlas_hydro.get_sensor_data()

    if hydroData is not None:
        for sensor in hydroData:
            print sensor
            jsonPackage = {
                'sensor_num': sensor['serial_number'],
                'hostname': gethostname(),
                'timestamp': 'Should-be-timestamp',
                'sensor_version': '1.00',
                'sensor_group': sensor['name'],
                'role': sensor['sensor_type'],
                'type': sensor['sensor_type']
            }

        hydrojson.extend(jsonPackage)

    print hydrojson
    return hydrojson

while True:
    format_data()
