#The GPIO.BOARD option specifies that you are referring to the pins by the number of the pin the the plug - i.e the numbers printed on the board (e.g. P1)
# and in the middle of the diagrams below.
#The GPIO.BCM option means that you are referring to the pins by the "Broadcom SOC channel" number, these are the numbers after "GPIO" in the green rectangles
# around the outside of the below diagrams:

import RPi.GPIO as GPIO
import time
import datetime
import os

light = False

GPIO.setmode(GPIO.BCM) 
GPIO.setup(4, GPIO.IN)
#GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
#A pull-down adds an additional resistor between the pin and ground, or put simply forces the voltage when the button is not pressed to be 0.

print GPIO.input(4)


def openLight(argument):
		global light
		print "Let's see if we take the command"
		millis = int(round(time.time() * 1000))
		newmillis = int(round(time.time() * 1000))
		soundPeack = 1
		while ( newmillis <= (millis + int(1000)) ):
			#print newmillis - millis
			#print GPIO.input(4)
			GPIO.remove_event_detect(4) 
			if GPIO.input(4):
				soundPeack = soundPeack + 1
				time.sleep(0.1) #give 100 ms to gpio pin rest time
			newmillis = int(round(time.time() * 1000))
		if soundPeack == 2:
			if light:
				os.system("sudo ../433Utils/RPi_utils/codesend 1135932") #close 
				light = False
			else:
				os.system("sudo ../433Utils/RPi_utils/codesend 1135923") #on
				light = True
			print "Good clap"
		else:
			print "Nope"
		print soundPeack
		GPIO.add_event_detect(4, GPIO.RISING, callback=openLight, bouncetime=300)

GPIO.add_event_detect(4, GPIO.RISING, callback=openLight, bouncetime=300)


#GPIO.add_event_callback(4, openLight)
try:
	mode = raw_input("What is the state of the light in the room? <on,off> \n ")
	
	if mode == "on":
		light = True
	else:
		light = False

	while True:
		time.sleep(5)

except KeyboardInterrupt:
	 GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  