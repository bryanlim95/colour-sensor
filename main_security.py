from tkinter import Tk, Frame, Label, Entry, Button, RIGHT, TOP, YES, X
import tkinter.messagebox as box
import random
import time

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

def des_encrypt(realText, step):
    outText = []
    uppercase = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for eachChar in realText:
        if eachChar in uppercase:
            index = uppercase.index(eachChar)
            crypting = (index + step) % 26
            newChar = uppercase[crypting]
            outText.append(newChar)

        elif eachChar in  digits:
            index = digits.index(eachChar)
            crypting = (index - step) % 10
            newChar = digits[crypting]
            outText.append(newChar)

        else:
            newChar = eachChar
            outText.append(newChar)

    random.shuffle(outText)

    return outText

step = 3

# An input is requested and stored in a variable


#Authentication

dig = []
digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


def dialog1():
    message = entry1.get()
    translated = des_encrypt(message, step)
    for eachChar in translated:
        if eachChar in digits:
            dig.append((int(eachChar)+step)%10)
    if (sum(dig) > 15):
        box.showinfo('info','Access Granted')
        #response = 'Access Granted'
        #time.sleep(2)
        window.destroy()
    else:
        box.showinfo('info','Access Denied')
        #response = 'Access Denied'
        #time.sleep(2)
        window.destroy()



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

Label3 = Label(window,text = 'Temp:')
Label3.pack(padx = 15,pady = 5)

btn.pack(side = RIGHT , padx = 5)
frame.pack(padx = 100,pady = 19)
window.mainloop()
