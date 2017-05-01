#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import numpy
import json
import gdrive_util as gu
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pymongo
from datetime import datetime, timedelta
import ftdi_hydro

gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)

while 1:
    print ftdi_hydro.get_sensor_data()
