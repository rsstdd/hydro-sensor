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

for sensor in sensors:
    print sensor..get_currentValue()

# print('TOP LEVEL')
# print (
#     '%2.2f' % tempT.get_currentValue() + "deg F   "
#     + "%2.1f" % humidT.get_currentValue() + "%  "
#     + str(int(lightT.get_currentValue())/82) + ' PAR'
# )
#
# print('TOP MID LEVEL')
# print (
#     '%2.2f' % tempTM.get_currentValue() + "deg F   "
#     + "%2.1f" % humidTM.get_currentValue() + "%  "
#     + str(int(lightTM.get_currentValue())/82) + ' PAR'
# )
#
# print('MID LOW LEVEL')
#
# print (
#     '%2.2f' % tempML.get_currentValue() + "deg F   "
#     + "%2.1f" % humidML.get_currentValue() + "%  "
#     + str(int(lightML.get_currentValue())/82) + ' PAR'
# )
#
# print('LOW LEVEL')
#
# print (
#     '%2.2f' % tempL.get_currentValue() + "deg F   "
#     + "%2.1f" % humidL.get_currentValue() + "%  "
#     + str(int(lightL.get_currentValue())/82) + ' PAR'
# )
#
# print '----------------'
# print ''
