#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from datetime import timedelta, date
import os, sys
# add ../sources to the PYTHONPATH
sys.path.append(os.path.join('./sources'))
import atlas_hydro

hydroData = atlas_hydro.get_sensor_data()


def format_data():
    hydrojson = []

    if hydroData is not None:
        for sensor in hydroData:
            if sensor["sensor_type"] == "atlas_scientific_ec":
                hydrojson.append({
                    'sensor_num': sensor['serial_number'],
                    'timestamp': 'Should-be-timestamp',
                    'sensor_version': '1.00',
                    'sensor_group': 'Production',
                    'role': sensor['sensor_type'],
                    'ec': sensor['sensor_reading'],
                })

                hydrojson.append({
                    'sensor_num': sensor['serial_number'],
                    'timestamp': 'Should-be-timestamp',
                    'sensor_version': '1.00',
                    'sensor_group': 'Production',
                    'role': sensor['sensor_type'],
                    'ppm': sensor['ppm']
                })

            else:
                hydrojson.append({
                    'sensor_num': sensor['serial_number'],
                    'timestamp': 'Should-be-timestamp',
                    'sensor_version': '1.00',
                    'sensor_group': 'Production',
                    'role': sensor['sensor_type'],
                    'sensor_reading': sensor['sensor_reading']
                })

    print hydrojson
    return hydrojson


format_data()
