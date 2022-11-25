import network

ssid = "George Hawkins AC"
password = "My incorrect password"

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(ssid, password)

status = -1
while not sta.isconnected():
    new_status = sta.status()
    if new_status != status:
        status = new_status
        print('Status', status)

print("Connected to {} with address {}".format(ssid, sta.ifconfig()[0]))