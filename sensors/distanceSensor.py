import RPi.GPIO as GPIO
import time

def checkIfSafeEncounter(distance, ownDeviceIsFound):
        print ("Detection found, Owner = %r" % ownDeviceIsFound)
        if distance < 20 and ownDeviceIsFound is not True:
                print ("Measured Distance = %.1f cm" % distance)
                return True
        return False

def getDistance(trigger, echo):
	checkTrigger(trigger)
	timeElapsed = calculateElapsedTime(echo)
	distance = (timeElapsed * 34300) / 2
	return distance

def checkTrigger(trigger):
	GPIO.output(trigger, True)
	time.sleep(0.00001)
	GPIO.output(trigger, False)

def calculateElapsedTime(echo):
	startTime = time.time()
	stopTime = time.time()

	while GPIO.input(echo) == 0:
		startTime = time.time()

	while GPIO.input(echo) == 1:
		stopTime = time.time()

	return stopTime - startTime
