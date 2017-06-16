import sys                   # RasPiO Inspiring scripts
from time import sleep       # http://rasp.io/inspiring
from gpiozero import MCP3008 # using analog upgrade
import apa
adc = MCP3008(channel=0, device=0)

numleds = 24                 # number of LEDs in our display

ledstrip = apa.Apa(numleds)
ledstrip.flush_leds()
ledstrip.zero_leds()
ledstrip.write_leds()

ledstrip.led_set(0, 255, 0, 0, 255)  #red led 0
ledstrip.led_set(1, 255, 255, 0, 0)  #blue led 1
ledstrip.led_set(2, 255, 0, 128, 0)  #green led 2
ledstrip.led_set(3, 255, 25, 25, 25) #dim white led 3
ledstrip.led_set(4, 255, 50, 0, 50)  #magenta led 4
ledstrip.led_set(5, 255, 50, 50, 0)  #cyan led 5
ledstrip.led_set(6, 255, 0, 50, 50)  #yellow led 6
ledstrip.led_set(7,   0, 10, 0, 0)   #black led 7 

ledstrip.write_leds()

print("""
This script reads channels 0-2 of the MCP3008 and converts the signal to
a number between 0 and 255.
Channel 0 = blue, 1 = green, 2 = red

Connect a 10k potentiometer so that the middle terminal goes to an ADC channel.
The other two terminals go to GND and 3V3. Do this for channels 0-2.

The LEDs are lit with the intensity determined by the analog inputs.
You can mix any colour on the RGB light spectrum by twiddling the pots.

You should get on-screen output and the LEDs' intensity will change
as you twiddle the pots. Have fun! And don't forget to tweak the script.

""")

sleep(1)

bgr_values = [0,0,0]       # blue, green, red
old_bgr_values = [1,1,125] # nonsense data starting point

try:
    while True:
        for x in range(0, 3):
            with MCP3008(channel=x) as reading:           # read the ADC
                bgr_values[x] = int(reading.value * 255)
            sleep(0.01)                     # rate limiter
            print ('\r', 'B:', 
                  "{0:03d}".format(bgr_values[0]), ' G:', 
                  "{0:03d}".format(bgr_values[1]), ' R:', 
                  "{0:03d}".format(bgr_values[2]), '\r', sep='', end='') 
            sys.stdout.flush()

        if bgr_values != old_bgr_values:    # only update LEDs if something changed
            for y in range(numleds):        # updating led_values directly
                ledstrip.led_values[y] = [255, bgr_values[0], bgr_values[1], bgr_values[2]]
            ledstrip.write_leds()       
        old_bgr_values = bgr_values[:]      # copy list without linking
        
finally:
    print("/nAll LEDs OFF - BYE!/n")
    ledstrip.zero_leds()
    ledstrip.write_leds()