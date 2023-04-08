

#First Module: Spoof MAC address


ifconfig wlan0 down
ifconfig eth0 down
ifconfig wlan0mon down

macchanger -r wlan0
macchanger -r eth0
macchanger -r wlan0mon

ifconfig wlan0 up
ifconfig eth0 up
ifconfig wlan0mon up

