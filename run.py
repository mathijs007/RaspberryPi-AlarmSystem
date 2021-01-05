import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
from sensors.distanceSensor import distance, checkDistance
from sensors.dht11Sensor import displayDHT11
from connection.bluetoothFile import lookForDevice
from connection.ledConnectionAzure import sendLedToAzure
import asyncio

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Setup variables
BS=False
alarmEncounter=False
timer = 10
ledR = 16
ledB = 18
button = 12
buzzer = 7
distanceTrigger = 11
distanceEcho = 13
nameOfDevice = "OnePlus Mathijs"

# Setup GPIO
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

def enableLock(state):
	GPIO.output(buzzer, True)
	alarmReset()

	if state==False:
		GPIO.output(ledR,True)
		GPIO.output(ledB,False)
		state=True
		sleep(.5)
	else:
		GPIO.output(ledR,False)
		GPIO.output(ledB,True)
		state=False
		sleep(.5)
	return state

def alarmReset():
	global timer
	global alarmEncounter
	alarmEncounter=False
	timer = 10
	GPIO.output(buzzer, False)

try:
	while True:
		BS = buttonPressed(BS)
		BS = scanCard(BS)
		displayDHT11()
		asyncio.run(sendLedToAzure(GPIO.input(ledR)))
		if BS == True:
			if alarmEncounter == True:
				if timer == 0:
					print("trespasser")
					GPIO.output(buzzer, True)
				else:
					timer -= 1
					print(timer)
			else:
				dist = distance(distanceTrigger, distanceEcho)
				isRightDevice = lookForDevice(nameOfDevice)
				alarmEncounter = checkDistance(dist, isRightDevice)
		#sleep(1)

finally:
	GPIO.output(ledR, False)
	GPIO.output(ledB, False)
	alarmReset()
	GPIO.cleanup()
