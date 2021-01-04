import RPi.GPIO as GPIO
import random
import time
import json
from datetime import datetime
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=IoTAlarm.azure-devices.net;DeviceId=IotDevice;SharedAccessKey=+Rt4fs6qCSGVTa9Uk/D0oNiEgPBTTO9D8LU/+JZcn2A="

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)

led_state = GPIO.input(16)
MSG_TXT = '{{"led_state": {led_state}, "tijd": {tijd}}}'

def iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
        while True:
            msg_txt_formatted = MSG_TXT.format(led_state=led_state, tijd=json.dumps(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
)
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
    iothub_client_telemetry_sample_run()
