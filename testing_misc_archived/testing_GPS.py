# Mic Recording Script
#HEY BRYCE!

def GPS():
    from time import sleep, time
    import adafruit_gps
    import datetime
    import board
    import busio
    import socket
    import serial
    uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=10)

    gps = adafruit_gps.GPS(uart, debug=False) # Use UART/pyserial

    # Turn on the basic GGA and RMC info (what you typically want)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

    # Set update rate to once a second (1hz) which is what you typically want.
    gps.send_command(b"PMTK220,1000")
    # device_hostname = socket.gethostname()
    # launch_time = datetime.datetime.now()
    # timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")
    # gpsPath = f'/home/pi/glinda_main/dataFiles/gps/{device_hostname}_gpsData_{timestr}.csv'
    # f = open(gpsPath,'a+')
    dat = []
    looptime = time()
    #try:
    print('Reading GPS...\n')
    blah = 1
    try:
        while 1:
            for j in range(9):
                for i in range(60):
                    gps.update()
                    # if blah == 1:
                    if gps.has_fix:
                        print([time(), gps.hour, gps.latitude, gps.longitude, gps.speed_knots, gps.fix_quality, gps.satellites])  # used this for testing - BL
                        # dat.append([time(), gps.hour, gps.latitude, gps.longitude, gps.speed_knots, gps.fix_quality, gps.satellites])
                    else:
                        print(([time(), 0, 0, 0, -1, -1, 0]))
                        # dat.append([time(), 0, 0, 0, -1, -1, 0])
                    sleep(1)
                #print('Writing... \n')
            #     for d in dat:
            #         f.write(str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) + ',' + str(d[3]) + ',' + str(d[4]) + ',' + str(d[5]) + '\n')
            #     #print('Closed.. \n')
            #     dat = []
            # f.close()
            # launch_time = datetime.datetime.now()
            # timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")
            # gpsPath = f'/home/pi/glinda_main/dataFiles/gps/{device_hostname}_gpsData_{timestr}.csv'
            # f = open(gpsPath,'a+')
            print('NEW GPS FILE')
    except KeyboardInterrupt:
        #f.close()
        print('\n Done Writing \n')
    except:
        print('ERROR')
        pass


if __name__ == '__main__':
    GPS()
