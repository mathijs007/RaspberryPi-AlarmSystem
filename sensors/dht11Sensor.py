import Adafruit_DHT
# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT11

# connected to GPIO17.
pin = 22

def displayDHT11():
	checkSensor()

def checkSensor():
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	if humidity is not None and temperature is not None:
    		checkForFire(temperature, humidity)
	else:
    		print('Failed to get reading. Try again!')

def checkForFire(temp, hum):
	if temp < 50:
		print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temp, hum))
	else:
		print('Too hot, calling fire department...')
