import RPi.GPIO as GPIO
import random
import time
import json
import asyncio
from datetime import datetime
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=IoTAlarm.azure-devices.net;DeviceId=IotDevice;SharedAccessKey=+Rt4fs6qCSGVTa9Uk/D0oNiEgPBTTO9D8LU/+JZcn2A="

MSG_TXT = '{{"led_state": {led_state}, "tijd": {tijd}}}'

def iothub_client_init():
    return IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

async def sendLedToAzure(led):
    client = iothub_client_init()
    msg_txt_formatted = MSG_TXT.format(led_state=led, tijd=json.dumps(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    message = Message(msg_txt_formatted)
    client.connect()
    print( "Sending message: {}".format(message))
    client.send_message(message)
    print ( "Message successfully sent" )
    client.disconnect()

#For running ledConnectionAzure.py independantly
def iothub_client_telemetry_sample_run(led):
    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
        while True:
            msg_txt_formatted = MSG_TXT.format(led_state=led, tijd=json.dumps(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            message = Message(msg_txt_formatted)
            
            print( "Sending message: {}".format(message))
            client.send_message(message)
            print ( "Message successfully sent" )
            time.sleep(3)
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run(1)
