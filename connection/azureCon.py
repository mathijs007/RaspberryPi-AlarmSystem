import RPi.GPIO as GPIO
import random
import time
import json
import asyncio
from datetime import datetime
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=IoTAlarm.azure-devices.net;DeviceId=IotDevice;SharedAccessKey=+Rt4fs6qCSGVTa9Uk/D0oNiEgPBTTO9D8LU/+JZcn2A="
MSG_TXT = '{{"led_state": {led_state}, "tijd": {tijd}}}'

async def sendLedToAzure(led):
	try:
		client = getClient()
		message = formatMessage(led)

		sendMessageToAzure(client, message)
	except:
		print("Can't send message")

def getClient():
	return IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

def formatMessage(led):
	formattedMsg = MSG_TXT.format(led_state=led, tijd=getCurrentTime())
	return Message(formattedMsg)

def getCurrentTime():
	return json.dumps(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def sendMessageToAzure(client, message):
	client.connect()
	print("Sending message: {}".format(message))
	client.send_message(message)
	print ("Message succesfully sent")
	client.disconnect()
