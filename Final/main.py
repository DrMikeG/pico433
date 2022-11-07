# I am programming and running this on a pico W using Thonny
import rp2
import network
import machine
import time
from secrets import secrets
from tx import TX
from rx import RX
import socket
import select

testMode = True

# Function to load in html page    
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
        
    return html

# Define blinking function for onboard LED to indicate error codes    
def blink_onboard_led(num_blinks):
    led = machine.Pin('LED', machine.Pin.OUT)
    for i in range(num_blinks):
        led.on()
        time.sleep(.2)
        led.off()
        time.sleep(.2)

blueLed= machine.Pin(18, machine.Pin.OUT)
blueLed.value(0)

touchSensorPinActiveHigh= machine.Pin(19,machine.Pin.IN, machine.Pin.PULL_DOWN) # directly connected to touch pad

led = machine.Pin('LED', machine.Pin.OUT)

# Use this to print the contents of remotes
#recv = RX(pin())
#recv.load('remotes')
#print(recv.keys())
#print(recv.show('2on'))
#print(recv.show('2off'))

# Set country to avoid possible errors
rp2.country('GB')

# Load login data from different file for safety reasons
ssid = secrets['ssid']
pw = secrets['pw']

transmit = TX(machine.Pin(16, machine.Pin.OUT), 'remotes', reps=10)
time.sleep(2)

response = get_html('index.html')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# Request fixed IP address of 192.168.0.97
wlan.ifconfig(('192.168.0.97', '255.255.255.0', '192.168.0.1', '8.8.8.8'))

while True:

    try :
        wlan_status = wlan.status()
        if wlan_status != network.STAT_GOT_IP:

            wlan.connect(ssid, pw)

            # Wait for connection with 10 second timeout
            timeout = 10
            while timeout > 0:
                if wlan.status() < 0 or wlan.status() >= 3:
                    break
                timeout -= 1
                print('Waiting for connection...')
                time.sleep(1)

            wlan_status = wlan.status()
            blink_onboard_led(wlan_status)

            if wlan_status != 3:
                #raise RuntimeError('Wi-Fi connection failed')
                print("Wi-Fi connection failed")
                time.sleep(30)
                continue
            else:
                print('Connected')
                status = wlan.ifconfig()
                print('ip = ' + status[0])
        else:
            print("Wifi already connected, reopening server socket")

        # HTTP server with socket
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

        # Create a "server socket":
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(addr)
        server_socket.listen(5)
        # The argument to listen tells the socket library that we want it to queue up 1 connect requests (the normal max) before refusing outside connections. 
        print("Listening on {} ".format(addr))

        switchOnCmd = 'L1On'
        switchOffCmd = 'L1Off'

        if testMode:
            switchOnCmd = '2on'
            switchOffCmd = '2off'

        lightOn = False

        inputs = [server_socket]
        outputs = []
        while inputs:
            #print('Non Blocking - waiting...')
            #print('.', end='')

            #print("Inputs list contains {} sockets".format(len(inputs)))
            readable,writable,exceptional = select.select(inputs,outputs,inputs,0.5)   
            #print("Select[readable,writable,exceptional] = {},{},{}".format(len(readable),len(writable),len(exceptional)))

            for s in writable:
                if s is server_socket:
                    print("Server socket is writable?")
                try :
                    # Send the stock response
                    print('Sending index.html')                
                    s.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                    print('Header sent')
                    s.sendall(response)
                    print('Response sent')
                    # Close the connection
                except Exception as error:
                    print("Socket write exception")
                    print(error)
                    outputs.clear()
                finally:
                    try :
                        print("Closing socket")
                        s.close()
                    except Exception as error:
                        print("Socket close")
                        print(error)
                    
                    if s in inputs:
                        inputs.remove(s)
                    if s in outputs:
                        outputs.remove(s)
                    break

            for s in readable:
                # Is there data on the server socket?
                # If so, we can use accept to get client_socket
                if s is server_socket:
                    print("Server socket is readable")
                    client_socket, address = server_socket.accept()
                    print("Connection from {}".format(address))
                    print("Adding to input list to read from")
                    # check if there is data on the client socket?
                    inputs.append(client_socket)
                    # Don't open more than one writable socket at once!
                    break
                else:
                    print("Client socket is readable")
                    # We have a client socket
                    print('Reading client socket')
                    data = s.recv(1024)
                    print('Read {} bytes'.format(len(data)))
                    # It is your responsibility to call recv again until your message has been completely dealt with.
                    # A protocol like HTTP uses a socket for only one transfer. The client sends a request, then reads a reply.
                    # That’s it. The socket is discarded. This means that a client can detect the end of the reply by receiving 0 bytes.            
                    if data:
                        print("Client socket had data / more data")
                        r = str(data[:50])
                        print(r)
                        led_on = r.find('?led=on')
                        led_off = r.find('?led=off')
                        led_toggle = r.find('?led=toggle')
                        print('led_on = ', led_on)
                        print('led_off = ', led_off)
                        print('led_toggle = ', led_toggle)
                        
                        if led_toggle > -1:
                            if lightOn:
                                led_off = 10
                            else:
                                led_on = 10
                        
                        if led_on > -1:
                            print("Transmit light on")
                            transmit(switchOnCmd)                
                            lightOn = True
                            blueLed.value(1)
                            
                        if led_off > -1:
                            print("Transmit light off")                
                            transmit(switchOffCmd)  # Immediate return
                            lightOn = False
                            blueLed.value(0)
                    else:
                        print("Couldn't read from client socket")
                        # Client socket now becomes an output
                        if s in inputs:
                            inputs.remove(s)        
                    
                    # Put the socket in the writables list, even if it's still get data to read?
                    if not s in outputs:
                        outputs.append(s)
                

            for s in exceptional:
                print('Non Blocking - error in {}'.format(s))
                if s in inputs:
                    inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                break
            
            print('.', end='')
            if touchSensorPinActiveHigh.value():
                time.sleep(0.1) # debounce
                if touchSensorPinActiveHigh.value():
                    if lightOn:
                        print("Transmit light off")                
                        transmit(switchOffCmd)  # Immediate return
                        lightOn = False
                        blueLed.value(0)
                        time.sleep(1) # prevent chatter
                    else:
                        print("Transmit light on")
                        transmit(switchOnCmd)                
                        lightOn = True
                        blueLed.value(1)
                        time.sleep(1)
    
    except Exception as error:
        print("Top level exception")
        print(error)
        break

print('Dropping into switch only mode', end='')
while True:
    time.sleep(0.1)
    if touchSensorPinActiveHigh.value():
        time.sleep(0.1) # debounce
        if touchSensorPinActiveHigh.value():
            if lightOn:
                print("Transmit light off")                
                transmit(switchOffCmd)  # Immediate return
                lightOn = False
                blueLed.value(0)
                time.sleep(1) # prevent chatter
            else:
                print("Transmit light on")
                transmit(switchOnCmd)                
                lightOn = True
                blueLed.value(1)
                time.sleep(1)