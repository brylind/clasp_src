# Author: Bryce Lindsey (bryce.lindsey@okstate.edu)
# Date: April 1 2022
# Description: Script that send data from GLINDA 2.0 to Google Drive
# ##############################################################################
# ##############################################################################

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ import the goodies ~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import socket
from time import sleep
import datetime
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
hname = socket.gethostname()  # get hostname for indexing
mic_data_path = f"/home/pi/glinda_main/dataFiles/mic"
gps_data_path = f"/home/pi/glinda_main/dataFiles/gps"
sleep(20)

try:
    while True:
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%m")
        day = datetime.datetime.now().strftime("%d")
        mic_remote_loc = f"{hname}/{hname}_mic_data/{year}/{month}/{day}"
        gps_remote_loc = f"{hname}/{hname}_gps_data/{year}/{month}/{day}"

        # move files using rclone (and a minimum age filter)
        comline_mic = f'rclone move "{mic_data_path}" "glinda_data:{mic_remote_loc}" --min-age 10m'
        os.system(comline_mic)
        os.system("echo mic data pushed to remote drive")
        comline_gps = f'rclone move "{gps_data_path}" "glinda_data:{gps_remote_loc}" --min-age 10m'
        os.system(comline_gps)
        os.system("echo gps data pushed to remote drive")
        sleep(600)
except:
    os.system("rclone push attempt failed")

