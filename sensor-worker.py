#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import numpy
import json
from datetime import datetime, timedelta
import ftdi_hydro

hydroData=ftdi_hydro.get_reading()

if hydroData is not None:
    print(hydroData)
    for item in hydroData:
        print(item)
else:
    print "err"

    #
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
