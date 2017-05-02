#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json
from datetime import timedelta, date
from socket import gethostname
import requests
import ftdi_hydro

hydroData = ftdi_hydro.read_sensors()


def format_data():
    if hydroData is not None:
        timestamp = datetime.datetime.now()
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

            hydrojson.append(jsonPackage)

    return hydrojson
