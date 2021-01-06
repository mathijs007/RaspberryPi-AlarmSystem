import os
import bluetooth

def lookForBluetoothDevice(name):
	try:
		devices = bluetooth.discover_devices(duration=10, lookup_names=1, flush_cache=1)
		return searchBetweenDevices(devices, name)
	except:
		return False

def searchBetweenDevices(devices, name):
	for device_address, device_name in devices:
		if device_name == name:
			print("Found your device: {}".format(device_name))
			return True
	return False
