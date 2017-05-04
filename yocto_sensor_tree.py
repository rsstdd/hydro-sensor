#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.join('./sources'))
from sensor_worker import dispatch_sensor_data

from yocto_api import *
from yocto_humidity import *
from yocto_temperature import *
from yocto_pressure import *
from yocto_lightsensor import *
import time


errmsg = YRefParam()

if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

# Top - lvl 1
# ------------
lightT = YLightSensor.FindLightSensor("LIGHTMK3-853DA.lightSensor")
humidT = YHumidity.FindHumidity('METEOMK1-7FB03.humidity')
tempT = YTemperature.FindTemperature('METEOMK1-7FB03.temperature')

# Top Middle - Lvl 2
# -------------------
lightTM = YLightSensor.FindLightSensor('LIGHTMK3-7CCBA.lightSensor')
humidTM = YHumidity.FindHumidity('METEOMK1-850EF.humidity')
tempTM = YTemperature.FindTemperature('METEOMK1-850EF.temperature')

# Middle - Lvl 3
# ---------------
lightML = YLightSensor.FindLightSensor('LIGHTMK3-7CAB6.lightSensor')
humidML = YHumidity.FindHumidity('METEOMK1-85165.humidity')
tempML = YTemperature.FindTemperature('METEOMK1-85165.temperature')

# Lower - Lvl 4
# --------------
lightL = YLightSensor.FindLightSensor('LIGHTMK3-85205.lightSensor')
humidL = YHumidity.FindHumidity('METEOMK1-7FA23.humidity')
tempL = YTemperature.FindTemperature('METEOMK1-7FA23.temperature')

sensors = [lightTM, humidTM, tempTM, lightML, humidML, tempML, lightL, tempL, humidL]

def get_tree_data:
    for sensor in sensors:
        if sensor.isOnline() is True:
            print ''
            print '%2.2f' % sensor.get_currentValue() + 'deg F   ' + '%2.1f' % sensor.get_currentValue() + '%  ' + str(int(sensor.get_currentValue()) / 82) + ' PAR'
