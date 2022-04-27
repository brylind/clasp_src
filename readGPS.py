# Mic Recording Script

def GPS():
    #################################
    # import the goodies
    from time import sleep, time
    import adafruit_gps
    import datetime
    import board
    import busio
    import socket
    import serial
    import urllib.request
    ########################################
    # device hostname is used all throughout this script
    device_hostname = socket.gethostname()

############################ SUPPORTING NESTED FUNCTIONS ############################################
    # def gpsTimestampFunc(gps_obj):
    #     gps_timestamp = 'None'
    #     now = time()
    #     while time() - now < 5:
    #         gps_obj.update()
    #         if gps_obj.has_fix:
    #             gps_obj.update()
    #             gps_time = (
    #                 f'{gps_obj.timestamp_utc.tm_hour}_{gps_obj.timestamp_utc.tm_min}_{gps_obj.timestamp_utc.tm_sec}')
    #             gps_timestamp = f'_GPS_UTCtimestamp_{gps_time}'
    #             return gps_timestamp
    #         else:
    #             pass

    def check_internet():
        try:
            _ = urllib.request.urlopen('https://www.google.com', None, timeout=5.1)
            print('GOOGLE reached (there is internet)')
            return True
        # except OSError:
        #     _ = urllib.request.urlopen('https://www.python.org', None, timeout=5.1)
        #     print('GOOGLE ping failed, python.org succeeded')
        #     return True
        except:
            print(f'no internet')
            return False

####################################################################################
    # now the fun begins
    uart = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=100)

    gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial
    # Turn on the basic GGA and RMC info (what you typically want)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

    # gps.send_command(b"PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0")

    # Set update rate to once a second (1hz) which is what you typically want.
    gps.send_command(b"PMTK220,10000")

    if check_internet():
        internet = ''
        # gps_timestamp = ''
    else:
        internet = 'NOINT_'
        # gps_timestamp = gpsTimestampFunc(gps)

    launch_time = datetime.datetime.now()
    timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")
    # gpsPath = f'/home/pi/glinda_main/dataFiles/gps/{internet}{device_hostname}_gpsData_{timestr}{gps_timestamp}.csv'
    gpsPath = f'/home/pi/glinda_main/dataFiles/gps/{internet}{device_hostname}_gpsData_{timestr}.csv'
    f = open(gpsPath, 'a+')
    dat = []

    try:
        while 1:
            f.write('Time_s' + ',' + 'Latitude' + ',' + 'Longitude' + ',' + 'Speed_kts' + ',' + 'GPS_fix' +
                    ',' + 'Satellites' + ',' + 'GPS_UTCtime_H_M_S' + '\n')
            for j in range(5):  # the range(#'s) are the size of the output file (when multiplied)
                for i in range(12):
                    gps.update()
                    if gps.has_fix:  # gps fix: 0=no, 1=yes, 2=differential fix
                        gps_time = (
                            f'{gps.timestamp_utc.tm_hour}_{gps.timestamp_utc.tm_min}_{gps.timestamp_utc.tm_sec}')
                        dat.append(
                            [time(), gps.latitude, gps.longitude, gps.speed_knots, gps.fix_quality,
                             gps.satellites, gps_time])
                    else:
                        dat.append([time(), 0, 0, -1, -1, 0, 0])
                    sleep(5)

                for d in dat:
                    f.write(str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) + ',' +
                            str(d[3]) + ',' + str(d[4]) + ',' + str(d[5]) + ',' + str(d[6]) + '\n')
                dat = []  # help clear out ram so "dat" can be refilled with data
            f.close()

            if check_internet():
                internet = ''
                # gps_timestamp = ''
            else:
                internet = 'NOINT_'
                # gps_timestamp = gpsTimestampFunc(gps)

            launch_time = datetime.datetime.now()
            timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")
            # gpsPath = f'/home/pi/glinda_main/dataFiles/gps/{internet}{device_hostname}_gpsData_{timestr}{gps_timestamp}.csv'
            gpsPath = f'/home/pi/glinda_main/dataFiles/gps/{internet}{device_hostname}_gpsData_{timestr}.csv'
            f = open(gpsPath, 'a+')
            print('NEW GPS FILE')

    except KeyboardInterrupt:
        f.close()
        print('\n Done Writing \n')
    except:
        print('ERROR')
        pass


if __name__ == '__main__':
    GPS()
