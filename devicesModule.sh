
rm devices-01.csv
airodump-ng -d $1 -c $2 -w ./devices --output-format csv wlan0mon



