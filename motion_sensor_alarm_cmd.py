#!/usr/bin/python

"By Philippe Akue"

#code tested on both python 2 and python 3
import RPi.GPIO as GPIO
import pygame
import time ; import datetime
import os
GPIO.setmode(GPIO.BCM)

#setting up LEDS
leds = (21, 23, 16, 12, 25, 24) #all pins being used for lights
GPIO.setup(leds,GPIO.OUT) #pins set as outputs







#setting up the PIR motion sensor
pir = 18 #GPIO pin used for the PIR sensor
GPIO.setup(pir, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #setting up the motion sensor as input with pull down resistor
#				default: the pin doesn't have current, when motion is detected: the pin gets current

#setting up alarm sound
pygame.mixer.init() #initializing pygame.mixer
alarm = pygame.mixer.Sound("Documents/alarm.wav") #creating the sound object for the alarm
#In python 3, you need to replace 'Documents/alarm.wav' by the full path of the file 'alarm.wav'


def countdown(): # function for countdown before arming the alarm
	t = int(raw_input("    To set the alarm, enter countdown value\n\t\t>"))
	print ("\n\nAlarm set in %s seconds") % t
	while t > 0:
		print (t)
		t -= 1
		GPIO.output(leds,GPIO.HIGH)
		time.sleep(0.1)
		GPIO.output(leds,GPIO.LOW)
		time.sleep(0.9)
		
try:
    os.system('clear') #from the command line, use the command 'clear'
    GPIO.output(leds,GPIO.LOW)
    while 1:
        print ("***Raspberry Pi Passive Infrared Alarm***\n\n\n")
        countdown()
        print ("\nMotion sensor enabled")
        GPIO.wait_for_edge(pir,GPIO.RISING) # wait for the signal from Key A to keep resume code
        GPIO.output(leds,GPIO.HIGH) #turn on lights
        alarm.play(loops =-1) #plays the sound object in an endless loop
        #.play() plays sound files in the background of the code.
        triggered_time = datetime.datetime.now() #register the time alarm was trigerred
        print ("!!!INTRUDER DETECTED!!!\n!!!Alarm Triggered!!!\n")
        print ("To disable the alarm, press Enter")
        input()
        GPIO.output(leds,GPIO.LOW) #turn off lights
        alarm.stop()# stop playback
        print ("Alarm disabled\n\n")
        print ("Alarm trigerred at " + str(triggered_time.strftime("%Y/%m/%d %H:%M:%S")) + "\n") # gives trigerred time with a format
        print ("To continue, press Enter")
        print ("To exit, press Ctrl+C")
        input()
        os.system('clear')

except KeyboardInterrupt: # exit if Ctrl+C
    GPIO.cleanup() # clean pins
    print ("\n*** Motion Sensor Alarm Turned OFF ***\n")
