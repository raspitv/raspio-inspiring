import time                    # This clock works with RasPiO InsPiRing Circle
from time import sleep         # http://rasp.io/inspiring
from datetime import datetime
import apa                     # RasPiO InsPiRing driver class
numleds = 24                   # number of LEDs in our display
brightness = 6                 # 0-31, 224-255 or 0xE0-0xFF
ledstrip = apa.Apa(numleds)    # initiate an LED strip

def wipe(brightness, b, g, r): # function for hourly etc. wipe animations
    for i in range(numleds):
        ledstrip.led_set(i, brightness, b, g, r)
        ledstrip.write_leds()
        sleep(0.03)
    sleep(0.25)
    ledstrip.zero_leds()
    ledstrip.write_leds()

print ('Press Ctrl-C to quit.')

try:
    while True:
        timenow = datetime.now()  # grab local time from the Pi
        hour = timenow.hour       # and process into hour min sec
        if hour >= 12:
            hour = hour - 12
        minute = timenow.minute
        second = float(timenow.second + timenow.microsecond/1000000)
        print(hour, minute, "{0:.3f}".format(second))

        ledstrip.led_set(hour*2, brightness, 0, 0, 255)      # 2 Red LEDs for the hour
        if hour == 0:
            ledstrip.led_set(23, brightness, 0, 0, 255)
        else:
            ledstrip.led_set(hour*2-1, brightness, 0, 0, 255)

        precise_minute = float(minute + second/60.0)
        ledstrip.led_set(int(precise_minute / 2.5) , brightness, 0, 255, 0) # green minute

        ledstrip.led_set(int(second / 2.5) , brightness, 255, 0, 0)         # blue second

        ledstrip.write_leds()

        # Now blank the LED values for all LEDs, so that if any values
        # change in the next loop iteration, we've cleaned up behind us
        ledstrip.zero_leds()
    
        time.sleep(0.03)   # limit the number of cycles to ~30 fps

        if minute == 59 and int(second) == 59:    # Red wipe hourly
            wipe(brightness, 0, 0, 255)
            
        elif minute == 29 and int(second) == 59:  # Green wipe half-hourly
            wipe(brightness, 0, 255, 0)
                                                  # Blue wipe quarter-hourly
        elif (minute == 14 or minute == 44) and int(second) == 59:
            wipe(brightness, 255, 0, 0)      
finally:
    print("/nAll LEDs OFF - BYE!/n")
    ledstrip.reset_leds()

"""
This 12-hour clock script takes the time from the system 
and breaks it down into hours minutes and decimal seconds.

If you have a monitor attached the time is displayed for
every iteration of the loop.

2 LEDs are used to show the hour in red
1 LED is used to show the nearest 2.5 minute (60/24 = 2.5)
1 LED denotes seconds (to the nearest 2.5)
Every hour there is a red 'round the clock' wipe animation
Every half hour there is a green 'round the clock' wipe animation
Every quarter hour there is a blue 'round the clock' wipe animation

You can tweak or customise the wipes or create new ones with
wipe(brightness, b, g, r)
"""