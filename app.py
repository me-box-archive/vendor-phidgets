#!/usr/bin/env python
import sys
sys.path.insert(0, "./lib")
from libDataboxDirectory import *
from phidgetsCallbacks import *


VENDER_NAME = "phidgets"

#register with databox
res = register_vendor(VENDER_NAME)
VENDER_ID = res['id']
ret = register_driver("driver_phidgets","The Super flexable phidgets ecosystem driver",VENDER_ID)
print ret



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

print("Press Enter to quit")
chr = sys.stdin.read(1)
print("Closing")
