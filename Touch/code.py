from machine import *
from utime import *
from tx import TX
from rx import RX
from rx.get_pin import pin

onBoardLed= Pin(25, Pin.OUT)
onBoardLed.value(0)

blueLed= Pin(18, Pin.OUT)
blueLed.value(0)

touchSensorPinActiveHigh= Pin(19,Pin.IN, Pin.PULL_DOWN) # directly connected to touch pad

# Use this to print the contents of remotes
#recv = RX(pin())
#recv.load('remotes')
#print(recv.keys())
#print(recv.show('2on'))
#print(recv.show('2off'))

transmit = TX(Pin(16, Pin.OUT), 'remotes', reps=10)
sleep(2)

testMode = False

switchOnCmd = 'L1On'
switchOffCmd = 'L1Off'

if testMode:
    switchOnCmd = '2on'
    switchOffCmd = '2off'

lightOn = False

while True:
    
    if touchSensorPinActiveHigh.value():
        sleep(0.1) # debounce
        if touchSensorPinActiveHigh.value():
            if lightOn:
                print("Transmit light off")                
                transmit(switchOffCmd)  # Immediate return
                lightOn = False
                blueLed.value(0)
                sleep(1) # prevent chatter
            else:
                print("Transmit light on")
                transmit(switchOnCmd)                
                lightOn = True
                blueLed.value(1)
                sleep(1)