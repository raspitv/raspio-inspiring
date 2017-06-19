import sys               # RasPiO Inspiring scripts
from time import sleep   # http://rasp.io/inspiring
import apa

numleds = 72             # number of LEDs in our display
delay = 0.03             # tweak to speed up or slow down
brightness = 10          # 0-31, 224-255, 0xE0-0xFF

ledstrip = apa.Apa(numleds)
if (brightness < 32):    # so you can use 0-31 for brightness too
    brightness += 224

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

try:
    while True:
        for y in range(numleds):
            ledstrip.led_values[y] = [brightness, ((y+1)*10 - (y // 24) * 240), 0, 0] # blue
            ledstrip.write_leds()
            sleep(delay)
        for y in range(numleds):
            ledstrip.led_values[y] = [brightness, 0, ((y+1)*10 - (y // 24) * 240), 0] # green
            ledstrip.write_leds()
            sleep(delay)
        for y in range(numleds):
            ledstrip.led_values[y] = [brightness, 0, 0, ((y+1)*10 - (y // 24) * 240)] # red
            ledstrip.write_leds()
            sleep(delay)
        for y in range(numleds):
            ledstrip.led_values[y] = [brightness, ((y+1)*10 - (y // 24) * 240), 0, ((y+1)*10 - (y // 24) * 240)] # magenta
            ledstrip.write_leds()
            sleep(delay)
        for y in range(numleds):
            ledstrip.led_values[y] = [brightness, ((y+1)*10 - (y // 24) * 240), ((y+1)*10 - (y // 24) * 240), 0] # cyan
            ledstrip.write_leds()
            sleep(delay)
        for y in range(numleds):
            ledstrip.led_values[y] = [brightness, 0, ((y+1)*10 - (y // 24) * 240), ((y+1)*10 - (y // 24) * 240)] # yellow
            ledstrip.write_leds()
            sleep(delay)
        for y in range(numleds):
            ledstrip.led_values[y] = [brightness, ((y+1)*10 - (y // 24) * 240), ((y+1)*10 - (y // 24) * 240), ((y+1)*10 - (y // 24) * 240)] # white
            ledstrip.write_leds()
            sleep(delay)
        
finally:
    print("/nAll LEDs OFF - BYE!/n")
    ledstrip.zero_leds()
    ledstrip.write_leds()
    
"""apasnake.py snakes its way round the pyramid from LED 0 to LED 71 
increasing the intensity by 10 for each successive LED on each triangle.
It cycles through a set sequence of colours.

You can do some very complex and flashy things with these LEDs
but once you've decided what you want to do, you have to devise 
some code to be able to do it.

apasnake.py starts to show you how you can use a mathematical
formula to loop through all the LEDs making them change the way
that you want.

What I wanted to do was vary the colour intensity of the LEDs on 
each triangle in the same way. The first one should have intensity 
of 10 and each one should increment 10 more. 
e.g. LED0=10, LED5=60, LED23=240

But I want the second triangle to be the same. 
So LED25 should be the same as LED0, LED47 same as LED23 etc.
This is what makes it slightly complex, but I figured it out.

The main 'guts' of this code is this bit here...

for y in range(numleds):
    ledstrip.led_values[y] = [brightness, ((y+1)*10 - (y // 24)*240), 0, 0] # blue
    ledstrip.write_leds()
    sleep(delay)

So we're looping through 0 to numleds, which is 0 to 72 on a pyramid.
The loop iterator y is the LED we're currently working on

So in the first iteration, y=0.
This gives us...
((y+1)*10 - (y // 24) * 240) 
(1*10 - (0 // 24) * 240)
(10 - 0) = 10

The // integer division is what makes this work the same for each triangle.
For triangle 1, LEDs 0-23,  (y // 24) * 240 = 0 * 240 = 0
For triangle 2, LEDs 24-47, (y // 24) * 240 = 1 * 240 = 240
For triangle 3, LEDs 48-71, (y // 24) * 240 = 2 * 240 = 480

for LED5 we get...
((y+1)*10 - (y // 24) * 240) 
(6*10 - (6 // 24) * 240)
(60 - 0) = 60

for LED47 (the last LED on triangle 2) it should give 240 
((y+1)*10 - (y // 24) * 240) 
(48*10 - (47 // 24) * 240)
(480 - (1 * 240) = 240

It can be quite hard (if you're not a mathematician) to work out what your 
formula should be, but just take it one step at a time, testing as you go.

The more you do it, the better you get at it too. This is where all that nasty
algebra we did in school shows its worth.
"""