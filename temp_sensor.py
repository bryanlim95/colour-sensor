import Adafruit_DHT
# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor = Adafruit_DHT.AM2302
gpio = 18
def temp_call() :
    humidity,temperature = Adafruit_DHT.read_retry(sensor, gpio)
    return humidity,temperature
