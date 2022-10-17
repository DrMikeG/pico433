import rp2
import network
import ubinascii
import machine
import urequests as requests
import time
from secrets import secrets
import socket

# Set country to avoid possible errors
rp2.country('GB')

# Load login data from different file for safety reasons
ssid = secrets['ssid']
pw = secrets['pw']

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.ifconfig(('192.168.0.97', '255.255.255.0', '192.168.0.1', '8.8.8.8'))
wlan.connect(ssid, pw)

# Wait for connection with 10 second timeout
timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)

# Define blinking function for onboard LED to indicate error codes    
def blink_onboard_led(num_blinks):
    led = machine.Pin('LED', machine.Pin.OUT)
    for i in range(num_blinks):
        led.on()
        time.sleep(.2)
        led.off()
        time.sleep(.2)

wlan_status = wlan.status()
blink_onboard_led(wlan_status)

if wlan_status != 3:
    raise RuntimeError('Wi-Fi connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    
# Function to load in html page    
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
        
    return html

# HTTP server with socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

# Create a "server socket":
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(addr)
s.listen(1)
# The argument to listen tells the socket library that we want it to queue up 1 connect requests (the normal max) before refusing outside connections. 

led = machine.Pin('LED', machine.Pin.OUT)

# Listen for connections
while True:
    try:
        # This blocks until a client connects
        cl, addr = s.accept()
        print('Client connected from', addr)
        # This recieves 1024 bytes - blocks until received
        r = cl.recv(1024)
        # print(r)
        
        r = str(r)
        led_on = r.find('?led=on')
        led_off = r.find('?led=off')
        print('led_on = ', led_on)
        print('led_off = ', led_off)
        if led_on > -1:
            print('LED ON')
            led.value(1)
            
        if led_off > -1:
            print('LED OFF')
            led.value(0)

        response = get_html('index.html')

        # blocks
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        # blocks
        cl.send(response)
        # blocks
        cl.close()
        
    except OSError as e:
        cl.close()
        print('Connection closed')