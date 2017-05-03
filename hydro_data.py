#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
# add ../sources to the PYTHONPATH
sys.path.append(os.path.join("..", "sources"))
import json
# from datetime import timedelta, date
import atlas_hydro


def format_data():
    hydroData = atlas_ftdi_hydro.read_sensors()

    if hydroData is not None:
        # timestamp = datetime.datetime.now()
        hydrojson = []

        for data in hydroData:

            jsonPackage = {
                'sensor_num': data['serial_number'],
                'hostname': gethostname(),
                'timestamp': 'Should-be-timestamp',
                'sensor_version': '1.00',
                'sensor_group': data['name'],
                'role': data['sensor_type'],
                'type': data['sensor_type']
            }

        print hydroData
        hydrojson.append(jsonPackage)

    return hydrojson
