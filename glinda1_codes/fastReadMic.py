# Mic Recording Script
#HEY BRYCE!

def mic():
    from adafruit_ads1x15.analog_in import AnalogIn
    from adafruit_ads1x15.ads1x15 import Mode
    import adafruit_ads1x15.ads1015 as ADS
    from time import time, sleep
    import datetime
    import board
    import busio

    i2c = busio.I2C(board.SCL, board.SDA)
    i2c = busio.I2C(board.SCL, board.SDA, frequency = 1000000)

    ads = ADS.ADS1015(i2c, data_rate = 3300, gain = 2/3)
    ads.mode = Mode.CONTINUOUS

    chan = AnalogIn(ads, ADS.P0, ADS.P1)
    s = 2 # seconds of recording

    launch_time = datetime.datetime.now()
    timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")
    micPath = "/home/pi/infrasound/dataFiles/micData" + timestr + ".csv"
    f = open(micPath, 'a+')
    dat = []
    looptime = time()
    #try:
    print('Reading...\n')
    try:
        while 1:
            for j in range(80):
                for i in range(int(2500*s)):
                    dat.append([time(), chan.voltage])
                    #if time()-looptime>0.00099:
                    #    append([time(), chan.voltage])
                    #    looptime = time()
                #print('Writing... \n')
                for d in dat:
                    f.write(str(d[0]) + ',' + str(d[1]) + '\n')
                #print('Closed.. \n')
                dat = []
            f.close()
            launch_time = datetime.datetime.now()
            timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")
            micPath = "/home/pi/infrasound/dataFiles/micData" + timestr + ".csv"
            f = open(micPath,'a+')
            print('NEW MIC FILE')
    except KeyboardInterrupt:
        f.close()
        print('\n Done Writing \n')
    except:
        print('ERROR')
        pass


if __name__ == '__main__':
    mic()
