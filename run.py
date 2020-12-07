import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

BS=False
ledR = 16
ledB = 18
button = 12

GPIO.setup(ledR, GPIO.OUT)
GPIO.setup(ledB, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
	if GPIO.input(button)==0:
		print("Button was pressed")
		return enableLock(state)
	return state

def enableLock(state):
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


try:
	while True:
		BS = buttonPressed(BS)
		BS = scanCard(BS)
finally:
	GPIO.output(ledR, False)
	GPIO.output(ledB, False)
	GPIO.cleanup()
