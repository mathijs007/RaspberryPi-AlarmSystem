import RPi.GPIO as GPIO
import os
import bluetooth

def lookForDevice(name):
	try:
		devices = bluetooth.discover_devices(duration=10, lookup_names=1, flush_cache=1)
		for device_address, device_name in devices:
			if GPIO.input(12)==GPIO.HIGH:
				break
			if device_name == name:
				print("Found your device: {}".format(device_name))
				return True
		return False
	except:
		return False 
