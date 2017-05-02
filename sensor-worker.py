#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import json
from datetime import datetime, timedelta
import ftdi_hydro

hydroData=ftdi_hydro.read_sensors()

print hydroData

if hydroData is not None:
    print '---------------------------'
    print hydroData
    print '---------------------------'
    print hydroData[0]
    print '---------------------------'
    print hydroData[1]
    print '---------------------------'
    print hydroData[2]['sensor_reading']
    print '---------------------------'
else:
    print "None error"



    # timestamp = datetime.datetime.now()
    #
    # jsonPackage={
    # 'sensor_num': sensor_num,
    # 'hostname' : gethostname(),
    # 'timestamp': timestamp,
    # 'hydro_temp': '',
    # 'hydro_ec': '',
    # 'hydro_ph': '',
    # 'hydro_flow': ''
    #  }
