#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.path.join("."))

import sys
from socket import gethostname

import json
from datetime import timedelta, date
import requests

import ftdi_hydro

print ftdi_hydro.get_ftdi_device_list()
