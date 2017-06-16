import spidev                  # RasPiO Inspiring scripts
from time import sleep         # http://rasp.io/inspiring
spi = spidev.SpiDev()
spi.open(0,1)   # using device 1 so 0 is free for AZ

class Apa(object):
    def __init__(self, numleds):
        self.numleds = numleds
        self.led_values = [] # initialise a list for LED values
        for y in range(numleds):
            self.led_values.append([0xE0, 0x00, 0x00, 0x00])

    def flush_leds(self):
        """Sends 4 null bytes to wake/initiate the APA102s
        also used to terminate the frame"""
        self.send = spi.xfer([0x00, 0x00, 0x00, 0x00])

    def write_leds(self):
        """write_leds() writes all stored led_values to LEDs"""
        self.flush_leds()
        for value in self.led_values:
            self.send = spi.xfer(value)
        for x in range((self.numleds // 32) +2):  #check this not overkill
            self.flush_leds()

    def reset_leds(self):    
        """reset_leds() switches all leds off manually 
        without changing stored led_values"""
        self.flush_leds()
        for x in range(self.numleds):
            """Set all APA102c LEDs to zero brightness 0xE0, 
            zero colour"""
            self.send = spi.xfer([0xE0, 0x00, 0x00, 0x00])
        for x in range((self.numleds // 32) +2):
            self.flush_leds()

    def zero_leds(self):
        """zero_leds() zeroes stored led_values 
        without writing their values to the LEDs. 
        i.e. total reset but don't display yet"""
        for y in range(self.numleds):
            self.led_values[y] = ([0xE0, 0x00, 0x00, 0x00])

    def led_set(self, number, brightness, blue, green, red):
        """led_set() is used to set the values for a specific LED.
        number is the list index of the LED
        e.g. first LED is 0 and eighth is 7.
        
        Brightness values are 0-31 for simplicity
        But you can also use  224-255 or 0xE0-0xFF
        
        Colour values are 0-255 in decimal or hex 0x00-0xFF.
        Values such as 255, 0, 0, 0 sometimes cause errors.
        
        If you want "black" or "off", better to use brightness of 224 or 0xE0
        then the LED will be off regardless of what colour values you give it
        """
        if (brightness < 32):   # so you can use 0-31 for brightness too
            brightness += 224
                
        self.led_values[number] = [brightness, blue, green, red]


if __name__ == "__main__":

    numleds = 24    # number of LEDs in our display

    ledstrip = Apa(numleds)
    print("flushing LEDS")
    ledstrip.flush_leds()
    print("Zeroing LEDS")
    ledstrip.zero_leds()
    print("Writing to LEDS")
    ledstrip.write_leds()

    print("Setting different colours to 8 LEDS (8th one is black = OFF)")
    ledstrip.led_set(0, 255, 0, 0, 255)  #red led 1
    ledstrip.led_set(1, 255, 255, 0, 0)  #blue led 2
    ledstrip.led_set(2, 255, 0, 128, 0)  #green led 3
    ledstrip.led_set(3, 255, 25, 25, 25) #dim white led 4
    ledstrip.led_set(4, 255, 50, 0, 50)  #magenta led 5
    ledstrip.led_set(5, 255, 50, 50, 0)  #cyan led 6
    ledstrip.led_set(6, 255, 0, 50, 50)  #yellow led 7
    ledstrip.led_set(7, 224, 0, 0, 0)    #black led 8 

    print("Writing to LEDS")
    ledstrip.write_leds()

    sleep(5)
    print("Resetting LEDS")
    ledstrip.reset_leds()
    

"""How it works...

import apa

You define the number of LEDs 

numleds = 20  and then call the class with...

ledstrip = apa.Apa(numleds)

ledstrip.flush_leds() sends 4 null bytes to spi 0 on CE1 to 'wake' the 
APA102c LEDs

Then you set the values of your LEDs
brightness, Blue, Green, Red

ledstrip.led_set(number, brightness, blue, green, red)
where number is the LED position number starting at 0

Brightness values are 0-31 for simplicity
But you can also use  224-255 or 0xE0-0xFF

RGB colour values are 0-255 decimal (or hex 0x00-0xFF)
Values such as 255, 0, 0, 0 sometimes cause errors.
        
If you want "black" or "off", better to use brightness of 0, 224 or 0xE0
then the LED will be off regardless of what colour values you give it
All LED values are stored in list variable
led_values

ledstrip.write_leds() initiates the SK9822 (or APA102c) LEDs, then writes
to spi the contents of led_values, namely 4 data bytes for each LED:
brightness, blue, green, red  

This sets the brightness and colours of each LED.

After that it sends (numleds // 32) +2 iterations of null data to
allow time for the LEDs at the end to catch up before writing to 
them again.

Default spi speed from spidev seems to be about 330 kHz.
This means that one transaction of 32 clock cycles, plus about 16
of time off in between should take about 48/330000 of a second.
Or you should be able to get 330000/48 = 6875 transactions per second.

There are three nulls between each frame.
With 20 LEDs you should therefore have 23 * 48/330000 = 3.3ms 
for each frame (ignoring Python processing time).
So a theoretical 300 frames per second. But Python slows it down.

I've noticed you can get about 100 counts per second.

You can squash in some more by upping the MHz, but only about 
3 times as many at 60 MHz. It looks like the chip enable process
slows things down. Perhaps xfer2 would be faster if no 
other SPI devices are in use?
"""