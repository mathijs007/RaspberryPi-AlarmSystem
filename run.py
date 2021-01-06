import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
from sensors.distanceSensor import getDistance, checkIfSafeEncounter
from sensors.dht11Sensor import displayDHT11
from connection.bluetoothCon import lookForBluetoothDevice
from connection.azureCon import sendLedToAzure
import asyncio

BS=False
alarmEncounter=False
timer = 10
ledR = 16
ledB = 18
button = 12
buzzer = 7
distanceTrigger = 11
distanceEcho = 13
bluetoothDevice = "OnePlus Mathijs"

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(ledR, GPIO.OUT)
GPIO.setup(ledB, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(distanceTrigger, GPIO.OUT)
GPIO.setup(distanceEcho, GPIO.IN)

def scanCard(state):
        reader = SimpleMFRC522()

        try:
                id, text = reader.read_no_block()
                if id==781013894693:
                        print("access")
                        return enableLock(state)
        finally:
                sleep(1)
        return state


def buttonPressed(state):
	if GPIO.input(button)==GPIO.HIGH:
		print("Button was pressed")
		return enableLock(state)
	return state

def switchState(state):
	if state==False:
		GPIO.output(ledR, True)
		GPIO.output(ledB, False)
		state=True
	else:
		GPIO.output(ledR, False)
		GPIO.output(ledB, True)
		state=False
	return state

def enableLock(state):
	state = switchState(state)
	resetAlarm()
	sleep(.5)
	return state

def resetAlarm():
	global timer
	global alarmEncounter
	alarmEncounter=False
	timer = 10
	GPIO.output(buzzer, False)

def useAlarm():
	global alarmEncounter
	if alarmEncounter == True:
		checkTimer()
	else:
		distance = getDistance(distanceTrigger, distanceEcho)
		isRightDevice = lookForBluetoothDevice(bluetoothDevice)
		alarmEncounter = checkIfSafeEncounter(distance, isRightDevice)

def checkTimer():
	global timer
	if timer == 0:
		print("Trespasser!")
		GPIO.output(buzzer, True)
	else:
		timer -= 2
		print(timer)

try:
	while True:
		BS = buttonPressed(BS)
		BS = scanCard(BS)
		displayDHT11()
		asyncio.run(sendLedToAzure(GPIO.input(ledR)))
		if BS == True:
			useAlarm()
		sleep(1)

finally:
	GPIO.output(ledR, False)
	GPIO.output(ledB, False)
	resetAlarm()
	GPIO.cleanup()
