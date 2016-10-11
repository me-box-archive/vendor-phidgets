#!/usr/bin/env python
import sys
import time
sys.path.insert(0, "./lib")
from libDataboxDirectory import *
from ctypes import *
import sys
import random
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit
from Phidgets.Phidget import PhidgetLogLevel
import math
import signal
import atexit



def shutdown():
    interfaceKit.closePhidget()
    print("done")

def signal_handler(signal, frame):
        shutdown()

atexit.register(shutdown)
signal.signal(signal.SIGINT, signal_handler)

DATASTORE_TIMESERIES_ENDPOINT = os.environ['DATASTORE_TIMESERIES_ENDPOINT']

VENDOR_NAME = "phidgets"
VENDOR_ID = None
DRIVER_ID = None
DATASTORE_ID = None


def valueToTemp(val):
    return (val/4) - 50

def valueToMovement(val):
    return (val * 0.22222) - 61.11

def valToHumidity(val):
    return ((val/1000) * 190.6) - 40.2

def valToLuminosity(val):
    return math.exp( (0.02356 * val) - 0.3762)

sensors = [
    {'sensor_type':"temp", 'unit': "Celsius", 'short_unit':"C", 'sensor_type_id':None, 'sensor_id': None, 'conversion': valueToTemp, 'description':"Phidgets sensor", 'location':'Unknown'},
    {'sensor_type':"humidity", 'unit': "percent", 'short_unit':"%", 'sensor_type_id':None, 'sensor_id': None, 'conversion': valueToMovement, 'description':"Phidgets sensor", 'location':'Unknown'},
    {'sensor_type':"luminosity", 'unit': "", 'short_unit':"lux", 'sensor_type_id':None, 'sensor_id': None, 'conversion': valToHumidity, 'description':"Phidgets sensor", 'location':'Unknown'},
    {'sensor_type':"movement", 'unit': "", 'short_unit':"", 'sensor_type_id':None, 'sensor_id': None, 'conversion': valToLuminosity, 'description':"Phidgets sensor", 'location':'Unknown'},
]

#register with databox
vendorRegisted = False
while not vendorRegisted:
    try:
        res = register_vendor(VENDOR_NAME)
        if 'id' in res:
            VENDOR_ID = res['id']
            ret = register_driver("databox-driver-phidgets","The Super flexable phidgets ecosystem driver",VENDOR_ID)
            if 'id' in ret:
                DRIVER_ID = ret['id']
                vendorRegisted = True
            else:
                raise Exception('')
        else:
            raise Exception('')
            
    except:
        print "ERROR: can't register with databox "
        time.sleep(2)


sensorsRegisted = False
while not sensorsRegisted:
    try:

        ret = get_datastore_id('datastore-timeseries')
        if 'id' in ret:
            DATASTORE_ID = ret['id']
        else:
            print ret
            raise Exception('get_datastore_id fail')

        print "DATASTORE_ID = " + str(DATASTORE_ID)
        
        for i in range(0,len(sensors)):
            ret = register_sensor_type(sensors[i]['sensor_type'])
            if 'id' in ret:
                sensors[i]['sensor_type_id'] = ret['id']
            else:
                print ret
                raise Exception('register_sensor_type fail')

            ret = register_sensor(DRIVER_ID, sensors[i]['sensor_type_id'], DATASTORE_ID, VENDOR_ID, sensors[i]['sensor_type'], sensors[i]['unit'], sensors[i]['short_unit'], sensors[i]['description'], sensors[i]['location'])
            if 'id' in ret:
                sensors[i]['sensor_id'] = ret['id']
            else:
                print ret
                raise Exception('register_sensor fial')
            
            sensorsRegisted = True
    except Exception as e:
        print "ERROR: can't register sensors with databox" 
        print e
        time.sleep(2)

def interfaceKitError(e):
    try:
        source = e.device
        print("InterfaceKit %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def interfaceKitInputChanged(e):
    source = e.device
    print("InterfaceKit %i: Input %i: %s" % (source.getSerialNum(), e.index, e.state))

def interfaceKitSensorChanged(e):
    source = e.device
    if len(sensors) > e.index:
        converter = sensors[e.index]['conversion']
        sensor_id = sensors[e.index]['sensor_id']
        value = converter(e.value)
        print("InterfaceKit %i: Sensor %i: %i" % (source.getSerialNum(), e.index, value))
        options = {
            'sensor_id': sensor_id, 
            'vendor_id': VENDOR_ID, 
            'value': value   
        }
        print "SENDING ------------------------"
        print options
        print "SENDING ------------------------"
        url = DATASTORE_TIMESERIES_ENDPOINT + '/reading'
        r = requests.post(url, data=options)
        ret = json.loads(r.content)
        print ret

def interfaceKitOutputChanged(e):
    source = e.device
    print("InterfaceKit %i: Output %i: %s" % (source.getSerialNum(), e.index, e.state))

try:
    interfaceKit = InterfaceKit()
    interfaceKit.setOnErrorhandler(interfaceKitError)
    interfaceKit.setOnInputChangeHandler(interfaceKitInputChanged)
    interfaceKit.setOnOutputChangeHandler(interfaceKitOutputChanged)
    interfaceKit.setOnSensorChangeHandler(interfaceKitSensorChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    interfaceKit.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Press Ctrl + c to quit")
while True:
    time.sleep(0.5)
print("Closing")



