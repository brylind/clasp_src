#!/bin/bash

cd /home/pi/infrasound/
while true; do
    sudo find /home/pi/infrasound/dataFiles -mtime +1 -delete
    sudo git add *
    now=$(date)
    sudo git commit -m "Automatic Push: $now"
    sleep 10
    sudo git push https://infrasoundOSU:MA3infrasound@github.com/Brandon-White-08/infrasound.git master
    sleep 300
done
