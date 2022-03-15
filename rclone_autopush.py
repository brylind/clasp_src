import os
import socket
from time import sleep

hname = socket.gethostname()
mic_data_path = f"/home/pi/glinda_main/dataFiles/mic"
gps_data_path = f"/home/pi/glinda_main/dataFiles/gps"
mic_remote_loc = f"{hname}/{hname}_mic_data"
gps_remote_loc = f"{hname}/{hname}_gps_data"
sleep(20)

try:
    while True:
        comline_mic = f'rclone move "{mic_data_path}" "glinda_data:{mic_remote_loc}" --min-age 10m'
        os.system(comline_mic)
        os.system("echo mic data pushed to remote drive")
        comline_gps = f'rclone move "{gps_data_path}" "glinda_data:{gps_remote_loc}" --min-age 30m'
        os.system(comline_gps)
        os.system("echo gps data pushed to remote drive")
        sleep(300)
except:
    os.system("rclone push attempt failed")

