import RPi.GPIO as GPIO
import random
import time

from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=IoTAlarm.azure-devices.net;DeviceId=IotDevice;SharedAccessKey=+Rt4fs6qCSGVTa9Uk/D0oNiEgPBTTO9D8LU/+JZcn2A="

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

led_state = GPIO.input(23)
MSG_TXT = '{{"led_state": {led_state}}}'

def iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
        while True:
            msg_txt_formatted = MSG_TXT.format(led_state=led_state)
            message = Message(msg_txt_formatted)

            if led_state == 0:
              message.custom_properties["ledAlert"] = "off"
            else:
              message.custom_properties["ledAlert"] = "on"

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
