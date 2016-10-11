import requests
import json
import os
import os.path

databox_directory_url = os.environ['DATABOX_DIRECTORY_ENDPOINT']

def register_driver(hostname, description, vendor_id):
	options = {
			 	"description": description,
			    "hostname": hostname,
			    "vendor_id": vendor_id
			 	}
	url = databox_directory_url +'/driver/register'
	r = requests.post(url, data=options)
	return json.loads(r.content)

def register_vendor(description):
	options = {"description": description}
	print databox_directory_url
	url = databox_directory_url +'/vendor/register'
	r = requests.post(url, data=options)
	return json.loads(r.content)


def register_sensor_type(description):
	options = {"description": description}
	url = databox_directory_url + '/sensor_type/register'
	r = requests.post(url, data=options)
	return json.loads(r.content)

def register_sensor(driver_id, sensor_type_id, datastore_id, vendor_id, vendor_sensor_id, unit, short_unit, description, location):
	options = 	{
					"description" : description, 
		            "driver_id": driver_id, 
		            "sensor_type_id" : sensor_type_id, 
		            "datastore_id" : datastore_id, 
		            "vendor_id" : vendor_id, 
		            "vendor_sensor_id" : vendor_sensor_id, 
		            "unit" : unit, 
		            "short_unit" : short_unit, 
		            "location" : location
				}
	url = databox_directory_url + '/sensor/register'
	r = requests.post(url, data=options)
	return json.loads(r.content)

def register_actuator_type(description):
	options = {"description": description}
	url = databox_directory_url + '/actuator_type/register'
	r = requests.post(url, data=options)
	return json.loads(r.content)

def register_actuator_method(actuator_id, description,):
	options = {
		"actuator_id" : actuator_id,
    	"description": description
	}
	url = databox_directory_url + '/actuator_method/register'
	r = requests.post(url, data=options)
	return json.loads(r.content)

def register_actuator(driver_id, actuator_type_id, controller_id, vendor_id, vendor_actuator_id, description, location):
	options = 	{
					"description" : description, 
		            "driver_id": driver_id, 
		            "sensor_type_id" : sensor_type_id, 
		            "datastore_id" : datastore_id, 
		            "vendor_id" : vendor_id, 
		            "vendor_sensor_id" : vendor_sensor_id, 
		            "unit" : unit, 
		            "short_unit" : short_unit, 
		            "location" : location
				}
	url = databox_directory_url + '/sensor/actuator'
	r = requests.post(url, data=options)
	return json.loads(r.content)

def get_my_registered_sensors(vendor_id):
	url = databox_directory_url+'/vendor/'+vendor_id+'/sensor'
	r = requests.get(url)
	return json.loads(r.content)

def get_datastore_id(hostname):
	options = {"hostname": hostname}
	url = databox_directory_url+'/datastore/get_id'
	r = requests.post(url, data=options)
	print r
	return json.loads(r.content)
