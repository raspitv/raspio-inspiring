# RasPiO Inspiring scripts
# http://rasp.io/inspiring

# Import our Python class called apa. 
# Your Python script needs to be in the same directory as apa.py
# (default is /home/pi/raspio-inspiring)
import apa, time

# Set the number of LEDs in our display. The class needs this.
numleds = 24   

# initialise LEDs
ledstrip = apa.Apa(numleds) 

ledstrip.flush_leds()

# set brightness value. 0 = OFF, 31 = FULL
brightness = 31 

# set LED 0 to full red
ledstrip.led_set(0, brightness, 0, 0, 255)

# write the currently stored values of the LEDs
# (the rest will still be zero as we've only changed one)
ledstrip.write_leds()

time.sleep(2)

# set all LED values to zero but don't 'write' them yet
ledstrip.zero_leds()

# set LED 4 to full RGB brightness
ledstrip.led_set(4, brightness, 255, 255, 255)
# write to the LEDs
ledstrip.write_leds()

time.sleep(2)

# switch off all LEDs just before we exit
ledstrip.reset_leds()

