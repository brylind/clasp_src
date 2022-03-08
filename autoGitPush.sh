#!/bin/bash
cd /home/pi/Documents/glinda2_proto/dataFiles
while true; do
    # DOES THIS SHOW (2/25)?
    # -mtime +2 is a positional argument specifying which files to look for based on when they were last modified
    # mtime +2 --> "modified time" is more than 2 day ago
    # The argument is called daystart - googling "linux daystart" helps
    # type "man find" for more info.. this line is just deleting data modified more than a day ago

  # todo: figure out how to insert hostname in bash file so it can be modular for each glinda2 unit
    sudo find /home/pi/Documents/glinda2_proto/dataFiles/GLINDA2pi_data -not -type d -mtime +10 -delete
    echo "Data files older than 10 minutes have been deleted"
    #sudo find /home/pi/Documents/glinda2_proto/dataFiles/GLINDA2pi_data -not -type d -mtime +1 -delete
    ## remove older files
    # sudo find .... -delete

    ## remove the "removed" files status from the working tree index
    # THIS NEEDS TO BE RESEARCHED AND REFINED (I GOT IT FROM STACKOVERFLOW)
    git ls-files --deleted -z | git update-index --assume-unchanged -z --stdin
    echo "Deleted files have been ignored for current git index"
    ## add all changes to the add stage from the working tree (with the deleted files removed with the previous section)
    git add .
    echo "Git add all"
    # git commit; git push
    # --------------------------------------------------------
    #sudo git add .
    now=$(date)
    echo "sleeping 10 seconds to allow files time to index"
    sleep 10    # sleep to allow files time to index into git working tree
    echo "10 second sleep done"
    git commit -m "Automatic Push: $now"
    echo "git commit 'automatic push' done"
    git push
    echo "initiate 5 minute sleep"
    sleep 300
done
