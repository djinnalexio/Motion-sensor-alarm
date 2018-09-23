#!/usr/bin/python

"by Philippe Akue"

#code tested on both python 2 and python 3
import RPi.GPIO as GPIO
import pygame
import time ; import datetime
import os
GPIO.setmode(GPIO.BCM)

#setting up LEDS
leds = (21, 23, 16, 12, 25, 24) #all pins being used for lights
GPIO.setup(leds,GPIO.OUT) #pins set as outputs

#setting up control buttons
keyA = 20 #pin being used for button A
keyB = 27 #pin being used for button B
GPIO.setup((keyA,keyB), GPIO.IN, pull_up_down = GPIO.PUD_UP) #setting up both keys as input with pull up resistor
#				default: the pins have current, when a key is pressed: that pin lose current

#setting up the PIR motion sensor
pir = 18 #GPIO pin used for the PIR sensor
GPIO.setup(pir, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #setting up the motion sensor as input with pull down resistor
#				default: the pin doesn't have current, when motion is detected: the pin gets current

#setting up alarm sound
pygame.mixer.init() #initializing pygame.mixer
alarm = pygame.mixer.Sound("Documents/alarm.wav") #creating the sound object for the alarm
#In python 3, you need to replace 'Documents/alarm.wav' by the full path of the file 'alarm.wav'


def countdown(t): # function for countdown before arming the alarm
    print ("\n***Alarm engaged in 10 seconds***\n")
	while t>0:
	    print ("\t\t%i\n") % t
        t -= 1 #means t = t -1 ; each time the section repeats, substracts 1 from t
        GPIO.output(leds,GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(leds,GPIO.LOW)
        time.sleep(0.9)

try:
    os.system('clear') #from the command line, use the command 'clear'
    GPIO.output(leds,GPIO.LOW)
    while 1:
        print ("***Raspberry Pi Passive Infrared Alarm***\n\n\n")
        print ("    To set the alarm, press Key A")
        GPIO.wait_for_edge(keyA,GPIO.FALLING) # wait for the signal from Key A to keep resume code
        countdown(10)
        print ("\n Motion sensor enabled!")
        GPIO.wait_for_edge(pir, GPIO.RISING) #wait for a signal from the PIR motion sensor
        GPIO.output(leds,GPIO.HIGH) #turn on lights
        alarm.play(loops =-1) #plays the sound object in an endless loop
        #.play() plays sound files in the background of the code.
        triggered_time = datetime.datetime.now() #register the time alarm was trigerred
        print ("!!!INTRUDER DETECTED!!!\n!!!Alarm Triggered!!!\n")
        print ("To disable the alarm, press Key 2")
        GPIO.wait_for_edge(keyB, GPIO.FALLING) #wait for the signal from Key 2 (pin 27) to keep going
        GPIO.output(leds,GPIO.LOW) #turn off lights
        alarm.stop()# stop playback
        print ("Alarm disabled\n\n")
        print ("Alarm trigerred at " + str(triggered_time.strftime("%Y/%m/%d %H:%M:%S")) + "\n") # gives trigerred time with a format
        print ("To continue, press Key 2")
        print ("To exit, press Ctrl+C, then press Key 2")
        GPIO.wait_for_edge(keyB, GPIO.FALLING)
        os.system('clear')

except KeyboardInterrupt: # exit if Ctrl+C
    GPIO.cleanup() # clean pins
    print ("\n*** Motion Sensor Alarm Turned OFF ***\n")
