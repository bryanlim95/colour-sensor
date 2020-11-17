import requests
import RPi.GPIO as GPIO
from gpiozero import MotionSensor
from picamera import PiCamera
from signal import pause
from filestack import Client
import time
import requests
request = None

client = Client('AfiwsCgmSHiNYVdEGYmSoz')
camera = PiCamera()
camera.resolution = (1920, 1080)
camera.rotation = 180
camera.framerate = 15

GPIO.setmode(GPIO.BOARD)
PIN_TRIGGER = 7
PIN_ECHO = 11
GPIO.setup(PIN_TRIGGER,GPIO.OUT)
GPIO.setup(PIN_ECHO,GPIO.IN)
GPIO.output(PIN_TRIGGER,GPIO.LOW)

def polling():
    GPIO.output(PIN_TRIGGER,GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER,GPIO.LOW)
    while GPIO.input(PIN_ECHO)==0:
        pulse_start = time.time()
    while GPIO.input(PIN_ECHO)==1:
        pulse_end = time.time()
    pulse_time = pulse_end - pulse_start
    distance1 = round(pulse_time * 17150, 2)   
    return distance1

def send_alert():
    #camera.capture('image.jpg')
    camera.start_recording('intruder.h264')
    camera.wait_recording(5)
    camera.stop_recording
    camera.close()
    client = Client("AfiwsCgmSHiNYVdEGYmSoz") #filestack api key = abcdefghijk
    new_filelink = client.upload(filepath='intruder.h264')
    print(new_filelink.url)
    r = requests.post('https://maker.ifttt.com/trigger/intruder/with/key/bZXKpF2Xl3ERNt3tlN4NX0', json={'value1' : new_filelink.url})
    if r.status_code == 200:
        print('Alert Sent')
    else:
        print('Error')


