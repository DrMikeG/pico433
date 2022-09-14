from machine import *
from utime import *
from tx import TX
from rx import RX

onBoardLed= Pin(25, Pin.OUT)
onBoardLed.value(0)

blueLed= Pin(18, Pin.OUT)
blueLed.value(0)

touchSensorPinActiveHigh= Pin(19,Pin.IN) # directly connected to touch pad

recv = RX(Pin(17, Pin.IN))
recv.load('remotes')
print(recv.keys())
print(recv.show('2on'))
print(recv.show('2off'))

transmit = TX(Pin(16, Pin.OUT), 'remotes', reps=10)
sleep(1)

lightOn = True

while True:
    
    if touchSensorPinActiveHigh.value():
        if lightOn:
            print("Transmit light on")
            transmit('2on')  # Immediate return
            lightOn = False
            blueLed.value(1)
            sleep(5)
        else:
            print("Transmit light off")
            transmit('2off')  # Immediate return
            lightOn = True
            blueLed.value(0)
            sleep(1)
    
    




