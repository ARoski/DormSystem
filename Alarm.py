from tkinter import *
from tkinter import ttk
import time
from pygame import mixer

##################################################################################
# Alec Rospierski
# Alarm Clock for Raspberry Pi
# v1.0 (most of the code is janky and can be fixed...probably at a later date)
# 7 - 16 - 18
##################################################################################

##################################################################################
# Functions that are connected to the buttons
##################################################################################

# Checks the time of the system every second & splits the system clock into two parts
def checkTime():
    tempList = timeFormat()
    partOne = tempList[0]
    partTwo = tempList[1]
    clockOne.config(text=partOne)
    clockTwo.config(text=partTwo)
    clockOne.after(1000, checkTime)

# Formats the time into two separate strings to be printed
def timeFormat():
    current = time.asctime(time.localtime(time.time()))
    temp = current.split(' ')
    partOne = temp[0:3]
    partTwo = temp[3:]
    return [partOne, partTwo]
    return temp

# Creates the Alarm with a pop-up screen
# (should probably be its own class)
def createAlarm():
    top = Toplevel(root)
    top.geometry("800x480")
    top.resizable(0, 0)
    canHandler = lambda: closeTop(top)
    close = Button(top, command=canHandler, text="Cancel")
    close.place(x=500, y=50)

    ########################################################
    hourOne = Label(top, text="0")
    hourOne.place(x=200, y=200)
    hourTwo = Label(top, text="0")
    hourTwo.place(x=230, y=200)
    minOne = Label(top, text="0")
    minOne.place(x=260, y=200)
    minTwo = Label(top, text="0")
    minTwo.place(x=290, y=200)
    ########################################################
    hOnePlusFun = lambda: addOne(hourOne, 2)
    hOneMinFun = lambda: subOne(hourOne)
    hTwoPlusFun = lambda: addOne(hourTwo, 9)
    hTwoMinFun = lambda: subOne(hourTwo)
    mOnePlusFun = lambda: addOne(minOne, 5)
    mOneMinFun = lambda: subOne(minOne)
    mTwoPlusFun = lambda: addOne(minTwo, 9)
    mTwoMinFun = lambda: subOne(minTwo)
    ########################################################
    hOnePlus = Button(top, command=hOnePlusFun, text="+")
    hOnePlus.place(x=200, y=170)
    hOneMin = Button(top, command=hOneMinFun, text="-")
    hOneMin.place(x=200, y=230)
    hTwoPlus = Button(top, command=hTwoPlusFun, text="+")
    hTwoPlus.place(x=230, y=170)
    hTwoMin = Button(top, command=hTwoMinFun, text="-")
    hTwoMin.place(x=230, y=230)
    
    mOnePlus = Button(top, command=mOnePlusFun, text="+")
    mOnePlus.place(x=260, y=170)
    mOneMin = Button(top, command=mOneMinFun, text="-")
    mOneMin.place(x=260, y=230)
    mTwoPlus = Button(top, command=mTwoPlusFun, text="+")
    mTwoPlus.place(x=290, y=170)
    mTwoMin = Button(top, command=mTwoMinFun, text="-")
    mTwoMin.place(x=290, y=230)
    ########################################################
    stop = lambda: saveAlarm(int(hourOne["text"]), int(hourTwo["text"]), int(minOne["text"]), int(minTwo["text"]), top)
    save = Button(top, command=stop, text="Set")
    save.place(x=500, y=80)
    
# Saves the alarm to the main display
def saveAlarm(one, two, three, four, top):
    closeTop(top)
    temp = "" + str(one) + str(two) + ":" + str(three) + str(four)
    currentAlarm.config(text=temp)
    alarmPlaying = False

# function to close the pop up window
def closeTop(top):
    top.destroy()

# Adds one time interval to the alarm
def addOne(display, num):
    temp = 0
    temp = int(display["text"])
    temp += 1
    if temp > num:
        display.config(text="0")
    else:
        display.config(text=str(temp))

# Subtracts one time interval to the alarm
def subOne(display):
    temp = int(display.cget("text"))
    temp -= 1
    if temp < 0:
        display.config(text="0")
    else:
        display.config(text=str(temp))
    
# Cancels the alarm if it is going off and if its waiting
def cancelAlarm():
    currentAlarm.config(text="")
    global alarmPlaying
    if alarmPlaying:
        mixer.music.stop()
        mixer.init()
        mixer.music.load("analog.mp3")
        alarmPlaying = False

# Snoozes the alarm for five minutes
def snoozeFunction():
    global alarmPlaying
    if alarmPlaying:
        mixer.music.stop()
        mixer.init()
        mixer.music.load("analog.mp3")
        alarmPlaying = False
    temp = currentAlarm.cget("text")
    one = int(temp[0])
    two = int(temp[1])
    three = int(temp[3])
    four = int(temp[4])
    four = four + 5
    if four > 9:
        three += 1
        four = 0
    if three > 5:
        two += 1
        three = 0
    if two > 9:
        one += 1
        two = 0
    if one > 2:
        one = 0
    var = "" + str(one) + str(two) + ":" + str(three) + str(four)
    currentAlarm.config(text=var)

alarmPlaying = False

# Sounds the alarm if it is time
def soundAlarm():
    global alarmPlaying
    alarm = currentAlarm.cget("text")
    currentTime = clockTwo.cget("text")
    if not alarmPlaying and alarm in currentTime and alarm != "":
        mixer.music.play()
        alarmPlaying = True
    clockOne.after(1000, soundAlarm)
##################################################################################

##################################################################################
# Setting up the main display
##################################################################################
# Creating the instance
root = Tk()

# Setting up the window
root.title("Work in Progress")
root.geometry("800x480")
root.resizable(0, 0)
mixer.init()
mixer.music.load("analog.mp3")

# Creating the Content
clockOne = Label(root, font=("Arial", 16))
clockTwo = Label(root, font=("Arial", 16))
snz = Button(root, command=snoozeFunction, text="SNOOZE")
setAlarm = Button(root, command=createAlarm, text="Set Alarm")
cancel = Button(root, command=cancelAlarm, text="Cancel Alarm")
currentAlarm = Label(root, font=16)

# Adding to the Content



# Placing the content
clockOne.place(x=50, y=50)
clockTwo.place(x=50, y=80)
snz.place(x=50, y=110)
setAlarm.place(x=50, y=140)
cancel.place(x=50, y=170)
currentAlarm.place(x=50, y=200)
##################################################################################

checkTime()
soundAlarm()
root.mainloop()
