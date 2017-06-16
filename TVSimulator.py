import time               # RasPiO Inspiring scripts
from time import sleep    # http://rasp.io/inspiring
from random import randint
import apa                # RasPiO InsPiRing driver class
numleds = 24              # number of LEDs in our display
brightness = 6            # 0-31, 224-255 or 0xE0-0xFF
max_brightness = 240      # 224-255 only

"""
This program emulates a TV by changing colours at random
time intervals in an attempt to make it look like
someone is at home watching TV.

It is eminently tweakable, so enjoy
"""

ledstrip = apa.Apa(numleds) # initiate an LED strip

ledstrip.flush_leds()  # initiate LEDs
ledstrip.zero_leds()
ledstrip.write_leds()

print ('Press Ctrl-C to quit.')

try:
    for x in range(numleds // 8):
        ledstrip.led_set(0+x*8, brightness, 0, 0, 255)  #red led 0
        ledstrip.led_set(1+x*8, brightness, 255, 0, 0)  #blue led 1
        ledstrip.led_set(2+x*8, brightness, 0, 80, 0)   #green led 2
        ledstrip.led_set(3+x*8, brightness, 30, 30, 30) #dim white led 3
        ledstrip.led_set(4+x*8, brightness, 50, 0, 50)  #magenta led 4
        ledstrip.led_set(5+x*8, brightness, 50, 50, 0)  #cyan led 5
        ledstrip.led_set(6+x*8, brightness, 0, 50, 50)  #yellow led 6
        ledstrip.led_set(7+x*8, brightness, 0, 5, 88)   #orange led 7 
	
    ledstrip.write_leds()
    sleep(1)
    
    counter = 0;
    iterations = 5;
    
    while True:
        if counter % iterations == 0:     # every 5 iterations do a longer one
            interval   = randint(150,300) # 15-30 seconds
            iterations = randint(3,8)     # change the iterations each longer one
            counter = iterations + 1      # ensure we get the full number of iterations
        else:
            interval   = randint(1,50)    # 0.1-5 seconds

        brightness = randint(225,max_brightness)
        red        = randint(0,55)
        green      = randint(0,255)
        blue       = randint(0,255)

        for x in range(numleds):
            ledstrip.led_set(x, brightness, blue , green, red)

        ledstrip.write_leds()
        print(counter, iterations, interval, brightness, blue, green, red)
        sleep(interval/10)
        counter += 1
        
finally:
    print("/nAll LEDs OFF - BYE!/n")
    ledstrip.zero_leds()
    ledstrip.write_leds()