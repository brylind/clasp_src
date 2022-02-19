# Mic Recording Script
#HEY BRYCE!

def IMU():
    import adafruit_lsm303_accel
    from time import time, sleep
    import datetime
    import board
    import busio

    i2c = busio.I2C(board.SCL, board.SDA, frequency = 1000000)

    accel = adafruit_lsm303_accel.LSM303_Accel(i2c)

    launch_time = datetime.datetime.now()
    timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")
    imuPath = "/home/pi/infrasound/dataFiles/imuData" + timestr + ".csv"
    f = open(imuPath,'a+')
    dat = []
    looptime = time()

    #print('Reading...\n')
    try:
        while 1:
            for j in range(5):
                for i in range(int(6000)):
                    dat.append([time(), accel.acceleration[0], accel.acceleration[1], accel.acceleration[2]])
                    sleep(0.01)
                for d in dat:
                    f.write(str(d[0]) + ',' + str(d[1])+ ',' + str(d[2]) + ',' + str(d[3])  + '\n')
                #print('Closed.. \n')
                dat = []
            f.close()
            launch_time = datetime.datetime.now()
            timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")
            imuPath = "/home/pi/infrasound/dataFiles/imuData" + timestr + ".csv"
            f = open(imuPath,'a+')
            print('NEW IMU FILE')
    except KeyboardInterrupt:
        f.close()
        print('\n Done Writing \n')
    except:
        print('ERROR')
        pass


if __name__ == '__main__':
    IMU()
