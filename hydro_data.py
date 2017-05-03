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

    print hydroData

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

        print hydrojson

        hydrojson.append(jsonPackage)

        # return hydrojson


format_data()
