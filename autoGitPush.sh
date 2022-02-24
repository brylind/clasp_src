#!/bin/bash

cd /home/pi/Documents/glinda2_proto/dataFiles
i=0
while i=0; do

    # -mtime +2 is a positional argument specifying which files to look for based on when they were last modified
    # mtime +2 --> "modified time" is more than 2 day ago
    # The argument is called daystart - googling "linux daystart" helps
    # type "man find" for more info.. this line is just deleting data modified more than a day ago
    sudo find /home/pi/Documents/glinda2_proto/dataFiles -mmin +60 -delete

    # sudo find /home/pi/Documents/glinda2_proto/dataFiles -mtime +1 -delete
    ## remove older files
    # sudo find .... -delete

    ## remove the "removed" files status from the working tree index
    # THIS NEEDS TO BE RESEARCHED AND REFINED (I GOT IT FROM STACKOVERFLOW)
    git ls-files --deleted -z | git update-index --assume-unchanged -z --stdin

    ## add all changes to the add stage from the working tree (with the deleted files removed with the previous section)
    sudo git add .

    # git commit; git push
    # --------------------------------------------------------
    #sudo git add .
    now=$(date)
    sleep 10
    sudo git commit -m "Automatic Push: $now"
    i=1
    #sleep 600
done
