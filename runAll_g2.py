# Author:   Brandon White (bcwhitecb@gmail.com)
# Date:     Feb 27, 2020
# Edit:     Mar 27, 2020
# Desc:     Reads and logs data from onboard sensors (listed below). For use on
#           Val Castor's storm chasing vehicle

# General Import Statements
import numpy as np
from multiprocessing import *
import board
import busio
from time import sleep, time
import datetime

# Set up I2C Address
i2c = busio.I2C(board.SCL, board.SDA)

#from fastReadIMU import IMU
#from fastReadGPS import GPS
from readMIC import mic

def launcher(i2c, runtime = -1):
    print('Main Launcher Started...')
    print('Runtime Selected: ' + str(runtime))
    print(' ')
    sleep(1)

    #Setup - List Processes
    print('Establishing Processes...')
    micRecorder = Process(target=mic, daemon = True)
    #gpsRecorder = Process(target=GPS, daemon = True)
    #imuRecorder = Process(target=IMU, daemon = True)
    sleep(2)
    print('***Processes Established \n')

    print('Launching Processes...')
    sleep(2)
    try:
        micRecorder.start()
        #gpsRecorder.start()
        #imuRecorder.start()
        launch_time = time()

        print('All Processes Started \n')

        while time() - launch_time < runtime or runtime == -1:
            sleep(5)
            pass

        print('Closing...')
        sleep(2)

        micRecorder.terminate()
        #gpsRecorder.terminate()
        #imuRecorder.terminate()
        micRecorder.join()
        micRecorder.join()
        #gpsRecorder.join()
        #imuRecorder.join()

        print('Processes Joined')

    except KeyboardInterrupt:
        micRecorder.terminate()
        #gpsRecorder.terminate()
        #imuRecorder.terminate()
        micRecorder.join()
        #gpsRecorder.join()
        #imuRecorder.join()
        print('Launcher Script Ended at Keyboad')
    #except:
        #micRecorder.terminate()
        #gpsRecorder.terminate()
        #imuRecorder.terminate()
        #micRecorder.join()
        #gpsRecorder.join()
        #imuRecorder.join()
        #print('Unknown Error in Launcher')


if __name__ == "__main__":
    launcher(i2c,-1)
