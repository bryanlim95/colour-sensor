from tkinter import Tk, Frame, Label, Entry, Button, RIGHT, TOP, YES, X
import tkinter.messagebox as box
import time
import math
import encryption
import trigger2
import threading

dig = []
digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
alert_dist = 30;


class Clock:
    def __init__(self):
        self.time1 = time.strftime('%H:%M:%S')
        self.mFrame = Frame()
        self.mFrame.pack(side=TOP,expand=YES,fill=X)
        self.watch = Label(self.mFrame, text=self.time1, font=('times',12,'bold'))
        self.watch.pack()
        self.changeLabel() #first call it manually

    def changeLabel(self):
        self.time1 = time.strftime('%H:%M:%S')
        self.watch.configure(text=self.time1)
        self.mFrame.after(200, self.changeLabel) #it'll call itself continuously
'''
class TempSensor:
    def __init__(self):
        (humidity,temp) = temp_sensor.temp_call()
        self.temp1 = round(temp,2)
        self.mFrame = Frame()
        self.mFrame.pack(side=TOP,expand=YES,fill=X)
        self.watch = Label(self.mFrame, text=self.temp1, font=('times',12,'bold'))
        self.watch.pack()
        self.changeLabel2() #first call it manually
        
    def changeLabel2(self):
        (humidity,temp) = temp_sensor.temp_call()
        self.temp1 = round(temp,2)
        self.mFrame = Frame()
        self.temp = temp_sensor.temp_call()
        self.watch.configure(text=self.temp1)
        self.mFrame.after(1000, self.changeLabel2) #it'll call itself continuously
'''
        
class Threading(object):
    def __init__(self, interval=2):
        self.interval = interval
        thread = threading.Thread(target=self.u_sensors, args=())
        thread.daemon = True
        thread.start()
        
    def u_sensors(self):
        while True:
            intrude = trigger2.polling()
            print(intrude)
            if intrude < alert_dist:
                if intrude > 0:          
                    trigger2.intruder_alert();                   
            time.sleep(self.interval)

def dialog1():
    message = entry1.get()
    translated = encryption.des_encrypt(message, 3)
    for eachChar in translated:
        if eachChar in digits:
            dig.append((int(eachChar)+3)%10)
    if (sum(dig) > 15):
        box.showinfo('info','Access Granted')
        tr = Threading()
        window.destroy()
    else:
        box.showinfo('info','Access Denied')

window = Tk()
window.title('Access Code')
frame = Frame(window)

Label1 = Label(window,text = 'Please Enter:')
Label1.pack(padx = 15,pady = 5)
entry1 = Entry(window,bd = 5)

entry1.pack(padx = 15, pady = 5)
btn = Button(frame, text = 'Authenticate',command = dialog1)

Label2 = Label(window,text = 'Current Time:')
Label2.pack(padx = 15,pady = 5)

obj1 = Clock()

Label3 = Label(window,text = 'Temp(C)')
Label3.pack(padx = 15,pady = 5)

#trigger2.main()

#obj2 = TempSensor()

btn.pack(side = RIGHT , padx = 5)
frame.pack(padx = 100,pady = 19)
window.mainloop()
