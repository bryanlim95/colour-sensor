import picamera 
import time
import numpy as np
import cv2
import imutils
import requests
import RPi.GPIO as GPIO
from filestack import Client
import requests
from pandas import read_csv
from sklearn.tree import DecisionTreeClassifier
import temp_sensor


# Variable definitions
PIN_TRIGGER = 7
PIN_ECHO = 11
dist_alert = 250
request = None

client = Client('AfiwsCgmSHiNYVdEGYmSoz')
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.rotation = 270

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_TRIGGER,GPIO.OUT)
GPIO.setup(PIN_ECHO,GPIO.IN)
GPIO.output(PIN_TRIGGER,GPIO.LOW)



#def main():
    #Start up
#bkgrd = bkgrd_save()
#time_bkgrd = time.time()

# Get trained Model
#model = train_model()
#    return bkgrd, model
''' 
    while(1):
        if time.time() > (time_bkgrd + (60*15)): #Update image every 15min due to light changes
            bkgrd = bkgrd_save()
            time_bkgrd = time.time()'''
        
def intruder_alert():
            # Send message on TELEGRAM intruder detected
            (humidity,temp) = temp_sensor.temp_call()       
            condition = environment(humidity,temp)
            r = requests.post('https://maker.ifttt.com/trigger/distance/with/key/bZXKpF2Xl3ERNt3tlN4NX0', json={'value1' : round(temp,1), 'value2' : round(humidity,1), 'value3' : condition})                  
            print(condition)
            obs_data = np.array([])
            
            #Record video
            obs_data = rec_dif(bkgrd, client)
            #print(obs_data)

            # Prediction
            if obs_data.size == 30:
                predictions = model.predict(obs_data.reshape(1,-1))
            else:
                predictions = model.predict(obs_data)
            print(predictions)
                #Send predictions to telegram
            requests.post('https://maker.ifttt.com/trigger/prediction/with/key/bZXKpF2Xl3ERNt3tlN4NX0', json={'value1' : predictions[0]})
        
def train_model ():
    names = ['x0', 'y0', 'a0', 'x1', 'y1', 'a1',  'x2', 'y2', 'a2', 'x3', 'y3', 'a3', 'x4', 'y4', 'a4', 'x5', 'y5', 'a5', 'x6', 'y6', 'a6', 'x7', 'y7', 'a7', 'x8', 'y8', 'a8',  'x9', 'y9', 'a9', 'class']
    dataset = read_csv("data1.csv", names=names)
    array = dataset.values
    X = array[:,0:30]
    y = array[:,30]
    model =  DecisionTreeClassifier()
    model.fit(X, y)
    print('Training done')
    return model

def video_preview():
    camera.start_preview()
    time.sleep(10)
    camera.close()
    
def bkgrd_save():
    # Capture background frame with no obstacles
    frame0 = np.empty((480, 640, 3), dtype=np.uint8)
    camera.capture(frame0, 'rgb')
    print("Background Updated")
    frame0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
    bkgrd = cv2.GaussianBlur(frame0, (21, 21), 0)
    return bkgrd        

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
        
def rec_dif(bkgrd, client):
    camera.start_recording('intruder.h264')
    obs = np.array([])
    cont = 1
    while (cont): # Continue recording
        obs_10 = np.array([])
        for i in range(10):
            frame = np.empty((480, 640, 3), dtype=np.uint8)
            camera.capture(frame, 'rgb', use_video_port = True)
            camera.wait_recording(0.4)
                    
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.GaussianBlur(gray, (21, 21), 0)

            # Compute difference between the 2 frames
            frameDelta = cv2.absdiff(bkgrd, frame)
            thresh = cv2.threshold(frameDelta, 50, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2) # dilate the thresholded image to fill in holes

            #Find contours
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            areas = np.array([])
            for c in cnts:
                areas = np.append(areas,cv2.contourArea(c))
                        
            if len(areas) > 1: # Take biggest box
                ind = np.argmax(areas)
                # compute the bounding box for the contour, draw it on the frame,
                (x, y, w, h) = cv2.boundingRect(cnts[ind])
                    
            else:
                if len(areas) == 1:
                    (x, y, w, h) = cv2.boundingRect(cnts[0])   
                            
                else:
                    x = 0
                    y = 0
                    w = 0
                    h = 0
                            
                                   
            obs_10 = np.append(obs_10, [x,y,w*h])
                
        if obs.size == 0:
            obs = obs_10
        else:
            if obs.size == 30:
                obs = np.append([obs], [obs_10], axis = 0)
            else:
                obs = np.append(obs, [obs_10], axis = 0)
        cont = 0
        
    camera.stop_recording()
    # Send video
    new_filelink = client.upload(filepath='intruder.h264')
    print(new_filelink.url)
    r = requests.post('https://maker.ifttt.com/trigger/intruder/with/key/bZXKpF2Xl3ERNt3tlN4NX0', json={'value1' : new_filelink.url})
    if r.status_code == 200:
        print('Alert Sent')
    else:
        print('Error')

    return obs

def environment(humidity,temp):
    
    lowTemp = "Temperature is lower than usual"
    highTemp = "Temperature is higher than usual"
    lowHum = "Humidity is lower than usual"
    highHum = "Humidity is higher than usual"
    normTemp = "Temperature is normal"
    normHum = "Humidity is normal"

    if (temp<20):
        OutputTemp = lowTemp
    elif (temp>25):
        OutputTemp = highTemp
    else:
        OutputTemp = normTemp

    if (humidity>50):
        OutputHum = highHum
    elif (humidity<40):
        OutputHum = lowHum
    else:
        OutputHum = normHum
    
    condition = OutputTemp+' , '+ OutputHum
    
    return condition

bkgrd = bkgrd_save()
time_bkgrd = time.time()

# Get trained Model
model = train_model()

