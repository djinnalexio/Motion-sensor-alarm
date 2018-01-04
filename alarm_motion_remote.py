#!/usr/bin/python
#By Philippe Akue
#code tested on both python 2 and python 3
import RPi.GPIO as GPIO
import pygame
import time ; import datetime
import os
GPIO.setmode(GPIO.BCM)

all = (21, 13, 16, 12, 25, 24) #all lights
GPIO.setup(all,GPIO.OUT) # setting the pins for lights as outputs

GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # setting up the PIR motion sensor as input with pull down resistor

pygame.mixer.init() #initializing pygame.mixer
alarm = pygame.mixer.Sound("/home/pi/Documents/alarm.wav") #creating the sound file for the alarm
#In python 3, you need to replace 'Documents/alarm.wav' by the full path of the file 'alarm.wav

def countdown(t): # function for countdown before arming the alarm
    while t>=0:
        print (t)
        t -= 1 # means t = t - 1
        GPIO.output(all,GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(all,GPIO.LOW)
        time.sleep(0.8)
    
try:
    os.system('clear') #from the command line, use the command 'clear'
    GPIO.output(all,GPIO.LOW)
    print ("***Raspberry Pi Passive Infrared Alarm***\n")
    while 1:
        print ("    To set the alarm, press Enter")
        input()
        print ("Alarm set in 10 seconds")
        countdown(10)
        print ("Motion sensor enabled")
        GPIO.wait_for_edge(18,GPIO.RISING) #wait for a signal from the PIR motion sensor to keep going
        GPIO.output(all,GPIO.HIGH) #turn on all lights
        alarm.play(loops =-1) #plays the sound file in an endless loop
        #.play() plays sound files in the background of the code.
        triggered_time = datetime.datetime.now() #register the time alarm was trigerred
        print ("!!!INTRUDER DETECTED!!!\n!!!Alarm Triggered!!!\n")
        print ("To disable the alarm, press Enter")
        input()
        GPIO.output(all,GPIO.LOW) #turn off all lights
        alarm.stop()# stop playback
        print ("Alarm disabled\n\n")
        print ("Alarm trigerred at " + str(triggered_time.strftime("%Y/%m/%d %H:%M:%S")) + "\n") # gives trigerred time with a format
        print ("To continue, press Enter")
        print ("To exit, press Ctrl+C")
        input()
        os.system('clear')

except KeyboardInterrupt: # exit if Ctrl+C
    GPIO.output(all,GPIO.LOW)
    GPIO.cleanup() # clean pins
    print ("\n***bye***\n")
