#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..","..","Sources"))

from yocto_api import *
from yocto_humidity import *
from yocto_temperature import *
from yocto_pressure import *
from yocto_lightsensor import *
from yocto_carbondioxide import *
import datetime
from yocto_datalogger import *
from oauth2client.service_account import ServiceAccountCredentials
import sys
from socket import gethostname

import json
import gspread
from datetime import timedelta, date
from pymongo import MongoClient
import requests

GDOCS_OAUTH_JSON       = 'oauth.json'

# Google Docs spreadsheet name.

GDOCS_SPREADSHEET_NAME = 'Solstice Environmental Data'

def login_open_sheet(oauth_key_file, spreadsheet):
    """Connect to Google Docs spreadsheet and return the first worksheet."""
    scope=['https://spreadsheets.google.com/feeds']
    try:
        json_key = json.load(open(oauth_key_file))
        credentials = ServiceAccountCredentials.from_json_keyfile_name(GDOCS_OAUTH_JSON , scope)
        gc = gspread.authorize(credentials)
        sh= gc.open(spreadsheet)
        worksheetTitle=str(target)
        try:
                worksheet = sh.worksheet(worksheetTitle)





        except Exception as ex:
                worksheet=sh.add_worksheet(title=worksheetTitle, rows="1", cols="15")
        return worksheet
    except Exception as ex:
        print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure sprea')
        print('Google sheet login failed with error:', ex)
        sys.exit(1)



def googleize(target,package):
    worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
    row=[datetime.datetime.now(),gethostname()]
    for data in package:
        row.append(data)
    try:
        worksheet.append_row(row)
        print (row)
    except Exception as ex:
            print('Google sheet append failed with error:', ex)

def mongoize(type,jsonPackage):
#	print jsonPackage
    filename="/var/local/thoth.id"
    deviceData['room']="Undefined"
    deviceData['role']="Undefined"

    with open(filename,"r") as file:
        deviceData=json.load(file)
        file.close()

    client = MongoClient('10.9.0.1')
    db=client.solstice
    collection=db[type]
    jsonPackage['type'] = type
    jsonPackage['room'] = deviceData['room']
    jsonPackage['role']=deviceData['role']
    sensorRecord = {"sensordata":jsonPackage}
    print sensorRecord
    try :
        record_id2=db.sensordata.insert_one(sensorRecord)
    except:
        with open('~thoth/sensordata.txt','w') as outfile:
            json.dump(jsonPackage, outfile)

    record_id=db[type].insert_one(jsonPackage).inserted_id
    #print record_id
    #print record_id2
#	print sensorRecord
    #send to heroku
    try:

        r = requests.post('https://luna-api.herokuapp.com/sensordata', data = jsonPackage)
        r2 = requests.post('https://luna-api-staging.herokuapp.com/sensordata', data = jsonPackage)
    except Exception as e:
        print e
errmsg = YRefParam()

# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + str(errmsg))

#print('Device list')












module = YModule.FirstModule()
while module is not None:
#    print(module.get_serialNumber() + ' (' + module.get_productName() + ')')
    target = module.get_serialNumber()
    moddesc=module.describe()
    if module.get_userVar() == 0:
       print  module.get_userVar()
       datalogger=YDataLogger.FindDataLogger(target)
       datalogger.set_timeUTC(datetime.datetime.utcnow())
       datalogger.set_autoStart(YDataLogger.AUTOSTART_ON)
       datalogger.set_recording(YDataLogger.RECORDING_ON)
       module.set_luminosity(0)
       print (module.set_userVar(1))
       print "Saving to flash"
       module.saveToFlash()
#    print moddesc

    module.set_luminosity(25)
    if "METEO" in moddesc:
    humSensor = YHumidity.FindHumidity(target + '.humidity')
    pressSensor = YPressure.FindPressure(target + '.pressure')
    tempSensor = YTemperature.FindTemperature(target + '.temperature')

#	print('%2.1f' % tempSensor.get_currentValue() + "°C   " +
#          "%4.0f" % pressSensor.get_currentValue() + "mb  " +
#          "%4.0f" % humSensor.get_currentValue() + "% ")
    temp= tempSensor.get_currentValue()
    press= pressSensor.get_currentValue()
    hum = humSensor.get_currentValue()
    sensor_num = target
    hostname = gethostname()
    timestamp = datetime.datetime.now()
#        googleize(target,package)
    jsonPackage={
    'sensor_num': sensor_num,
    'hostname' : hostname,
    'timestamp': timestamp,
    'temperature': temp,
    'pressure': press,
    'humidity': hum
     }
    mongoize('meteo', jsonPackage)
    es = 0.6108 * exp((2.5e6 /461) * (1/273 -1/(273 +temp) ) )

    vpd = es * (100 - hum)/100
    print vpd
    vpdPackage={
        'sensor_num': sensor_num,
        'hostname' : hostname,
        'timestamp': timestamp,
    'vpd': vpd
    }
    mongoize('vpd', vpdPackage)

    if "LIGHT" in moddesc:
    sensor= YLightSensor.FindLightSensor(target + '.lightSensor')
#	print("Light :  "+ str(int(sensor.get_currentValue()))+" lx ")
#	googleize(target,[sensor.get_currentValue()])
        jsonPackage={
        'sensor_num': target,
        'hostname' : gethostname(),
        'timestamp': datetime.datetime.now(),
        'lux': sensor.get_currentValue(),
         }
    mongoize('light',jsonPackage)



    if "CO2" in moddesc:
    sensor= YCarbonDioxide.FindCarbonDioxide(target+'.carbonDioxide')
#	print("CO2 :" + str(int(sensor.get_currentValue()))+" ppm")
#        googleize(target,[sensor.get_currentValue()])
        jsonPackage={
        'sensor_num': target,
        'hostname' : gethostname(),
        'timestamp': datetime.datetime.now(),
        'co2': sensor.get_currentValue(),
         }
        mongoize('co2',jsonPackage)




    module.set_luminosity(0)
    module = module.nextModule()
