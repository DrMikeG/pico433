from machine import *
from utime import *
from tx import TX

led= Pin(25, Pin.OUT)
led.value(0)

led2= Pin(18, Pin.OUT)
led2.value(0)

t1= Pin(19,Pin.IN) # directly connected to touch pad
sleep(1)

transmit = TX(pin(), 'remotes', reps=10)

trigLevel= 0


while True:

    led2.value(t1.value())
    if t1.value():
        transmit('2on')  # Immediate return
        sleep(5)
        transmit('2off')  # Immediate return
        sleep(1)
    
    



