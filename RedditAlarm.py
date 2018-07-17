from tkinter import *
from tkinter import ttk
import time
from pygame import mixer
import praw
import re

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

def scanReddit():
    submission = []
    for x in subreddit.new(limit=1):
        submission.append(x)
    #submission = subreddit.new(limit=1)
    #submission[0].comments.replace_more(limit=1)
    all_comments = submission[0].comments.list()
    #all_comments = submission[0].get_comments()
    if all_comments:
        temp = str(all_comments[0].body)
    else:
        temp = ""
    if submission[0].title == "Alarm" or submission[0].title == "alarm":
        if not temp == "Alarm Set": #currentAlarm.cget("text") != submission.selftext:
            currentAlarm.config(text=submission[0].selftext)
            submission[0].reply("Alarm Set")
    clockOne.after(30000, scanReddit)


##################################################################################
# Setting up the main display
##################################################################################
# Creating the instance
root = Tk()
reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit("BotUniversity")
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
cancel = Button(root, command=cancelAlarm, text="Cancel Alarm")
currentAlarm = Label(root, font=16)

# Adding to the Content



# Placing the content
clockOne.place(x=50, y=50)
clockTwo.place(x=50, y=80)
snz.place(x=50, y=110)
cancel.place(x=50, y=170)
currentAlarm.place(x=50, y=200)
##################################################################################

scanReddit()
checkTime()
soundAlarm()
root.mainloop()
