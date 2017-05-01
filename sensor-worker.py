#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import ftdi_hydro

while 1:
    print ftdi_hydro.get_sensor_data()
