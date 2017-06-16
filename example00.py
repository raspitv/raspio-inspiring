import apa                          # import apa module
ledstrip = apa.Apa(24)              # set up 24 LEDs
ledstrip.led_set(3, 31, 0, 255, 0)  # set LED 3 value to full green
ledstrip.write_leds()               # send values to all LEDs

# RasPiO Inspiring scripts
# http://rasp.io/inspiring