import os
import socket
from time import sleep

hname = socket.gethostname()
mic_data_path = f"/home/pi/glinda_main/dataFiles/mic"
gps_data_path = f"/home/pi/glinda_main/dataFiles/gps"
mic_remote_loc = f"{hname}/{hname}_mic_data"
gps_remote_loc = f"{hname}/{hname}_gps_data"

try:
    comline_mic = f'rclone move "{mic_data_path}" "glinda_data:{mic_remote_loc}" --min-age 2m'
    os.system(comline_mic)

    comline_mic = f'rclone move "{gps_data_path}" "glinda_data:{gps_remote_loc}" --min-age 2m'
    os.system(comline_mic)

    sleep(300)
except:
    os.system("rclone push attempt failed")

