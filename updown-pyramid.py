from time import sleep    # RasPiO Inspiring scripts
import apa                # http://rasp.io/inspiring

numleds = 72              # number of LEDs in our display
delay = 0.04
brightness = 5            # 0-31, 224-255, 0xE0-0xFF

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
sleep(1)

ledstrip.flush_leds()
ledstrip.zero_leds()
ledstrip.write_leds()

if (brightness < 32):   # so you can use 0-31 for brightness too
    brightness += 224

levels = [[16,17,18,19,20,21,22,23,40,41,42,43,44,45,46,47,64,65,66,67,68,69,70,71],
          [0,15,24,39,48,63],
          [1,14,25,38,49,62],
          [2,13,26,37,50,61],
          [3,12,27,36,51,60],
          [4,11,28,35,52,59],
          [5,10,29,34,53,58],
          [6,9,30,33,54,57],
          [7,8,31,32,55,56]]

backwards = levels[:]  # copy list and reverse it      
backwards.reverse()    # so we can easily go backwards

def updown(b,g,r):
    for level in levels:
        for led in level:
            ledstrip.led_values[led] = [brightness, b, g, r]
        ledstrip.write_leds()
        sleep(delay)
    for level in backwards:
        if len(level) != 24:       # prevents flicker on first level
            for led in level:
                ledstrip.led_values[led] = [brightness, 0, 0, 0]
        ledstrip.write_leds()
        sleep(delay)   

try:
    while True:
        updown(255,0,0)
        updown(0,255,0)
        updown(0,0,255)
        updown(255,255,0)
        updown(0,255,255)
        updown(255,255,255)
        #delay = delay * 0.9    # speed up a little bit each iteration

finally:
    print("/nAll LEDs OFF - BYE!/n")
    ledstrip.zero_leds()
    ledstrip.write_leds()

"""
This program cycles up and down the pyramid, changing colours for each iteration.

Things of note are...

levels (line 33) is a list of lists. 
Each element of the main list contains a list of LED numbers on the same level.
e.g. levels[0] contains 24 elements because there are 3 strips of 8 LEDs on that level.
All the other levels have 6 elements.

By grouping them in levels, we are able to control each level separately.

We do this by iterating through the levels and through the LEDs on each level
using nested loops...
    for level in levels:
        for led in level:
            ledstrip.led_values[led] = [brightness, b, g, r]

Then we manipulate ledstrip.led_values directly as this makes it easy for us to
directly over-write the values for the LEDs without using ledstrip.led_set()

The rest of the program is very similar to example03.py 
(in fact I ripped the code from updown_pyramid when I wrote example03.py
"""


