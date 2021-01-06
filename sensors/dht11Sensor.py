import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
dhtPin = 22

def displayDHT11():
	humidity, temperature = Adafruit_DHT.read_retry(sensor, dhtPin)

	if humidity is not None and temperature is not None:
    		checkForFire(temperature, humidity)
	else:
    		print('Failed to get reading. Try again!')

def checkForFire(temp, hum):
	if temp < 50:
		print('Temperature={0:0.1f}*C  Humidity={1:0.1f}%'.format(temp, hum))
	else:
		print('Too hot, calling fire department...')
