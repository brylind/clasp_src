#!/bin/bash

cd /home/pi/infrasound/
while true; do

    # -mtime +1 is a positional argument specifying which files to look for based on when they were last modified
    # mtime +1 --> "modified time" is more than 1 day ago
    # The argument is called daystart - googling "linux daystart" helps
    # type "man find" for more info.. this line is just deleting data modified more than a day ago
    sudo find /home/pi/infrasound/dataFiles -mtime +2 -delete

    #----------- Bryces addition (this needs to be tested) -------------
    ## remove older files
    # sudo find .... -delete

    ## remove the "removed" files status from the working tree index
    # THIS NEEDS TO BE RESEARCHED AND REFINED (I GOT IT FROM STACKOVERFLOW)
    git ls-files --deleted -z | git update-index --assume-unchanged -z --stdin

    ## add all changes to the add stage from the working tree (with the deleted files removed with the previous section)
    sudo git add .;

    git commit; git push
    # ----------------------------
    sudo git add *
    now=$(date)
    sudo git commit -m "Automatic Push: $now"
    sleep 10
    sudo git push https://infrasoundOSU:MA3infrasound@github.com/Brandon-White-08/infrasound.git master
    sleep 300
done
