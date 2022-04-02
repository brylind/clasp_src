# Mic Recording Script

def GPS():
    from time import sleep, time
    import adafruit_gps                             
    import datetime
    import board
    import busio
    import socket
    import serial
    import urllib.request
    
    def gpsTimestampFunc(gps):
        gps_timestamp = 'None'
        now = time()
        while time()-now < 5:
            if gps.has_fix:
                gps.update()
                gps_time = (f'{gps.timestamp_utc.tm_hour}_{gps.timestamp_utc.tm_min}_{gps.timestamp_utc.tm_sec}')
                # gps_time = datetime.datetime(gps.timestamp_utc.tm_year,\
                #     gps.timestamp_utc.tm_mon,\
                #     gps.timestamp_utc.tm_mday,\
                #     gps.timestamp_utc.tm_hour,\
                #     gps.timestamp_utc.tm_min,\
                #     gps.timestamp_utc.tm_sec)  
                # print(gps_time)
                gps_timestamp = (f'_GPS_UTCtimestamp_{gps_time}')
                return gps_timestamp                
            else:
                pass
            # function used after checking for internet (if no internet, return the gps fix timestamp for a reference)
        # this gps timestamp will not change if the gps maintain fix. But, it can be used to find the offset between the
        # the GPS time and the system time (which will be way off without internet connection)

    
    uart = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=100)
    
    gps = adafruit_gps.GPS(uart, debug=False) # Use UART/pyserial
    # Turn on the basic GGA and RMC info (what you typically want)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    
    # gps.send_command(b"PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0")

    # Set update rate to once a second (1hz) which is what you typically want.
    gps.send_command(b"PMTK220,2000")

    device_hostname = socket.gethostname()

    try:
        urllib.request.urlopen('http://google.com', None, timeout=5.1)
        internet = ''
        gps_timestamp = ''
    except:
        internet = 'NOINT_'
        print('no internet identified')
        gps_timestamp = gpsTimestampFunc(gps)
        print('GPS timestamp function done')

    launch_time = datetime.datetime.now()
    timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")
    gpsPath = f'/home/pi/glinda_main/dataFiles/gps/{internet}{device_hostname}_gpsData_{timestr}{gps_timestamp}.csv'
    f = open(gpsPath,'a+')
    dat = []

    try:
        while 1:
            for j in range(1):      # the range(#'s) are the size of the output file (when multiplied)
                for i in range(60):
                    gps.update()
                    if gps.has_fix:     #gps fix: 0=no, 1=yes, 2=differential fix
                        dat.append([time(), gps.latitude, gps.longitude, gps.speed_knots, gps.fix_quality, gps.satellites])
                    else:
                        dat.append([time(), 0, 0, -1, -1, 0])
                    sleep(1)
                #print('Writing... \n')        
            # if gps.has_fix:
            #     gps.update()
      
            #     delta_t = (datetime.datetime.utcnow()-gps_time).total_seconds()
            # else:
            #     delta_t = 'N/A'
            # f.write('Delta_t_sys_minus_gps_at_write' + ',' + str(delta_t) + '\n')

            f.write('Time_s' + ',' + 'Latitude' + ',' + 'Longitude' + ',' + 'Speed_kts' + ',' + 'GPS_fix' + ',' + 'Satellites' + '\n')
            for d in dat:
                f.write(str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) + ',' + str(d[3]) + ',' + str(d[4]) + ',' + str(d[5]) + '\n')
            #print('Closed.. \n')
            dat = []
            f.close()

            try:
                urllib.request.urlopen('http://google.com', None, timeout=5.1)
                internet = ''
                gps_timestamp = ''
            except:
                internet = 'NOINT_'
                print('no internet identified')
                gps_timestamp = gpsTimestampFunc(gps)
                print('GPS timestamp function done')

            launch_time = datetime.datetime.now()
            timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")
            gpsPath = f'/home/pi/glinda_main/dataFiles/gps/{internet}{device_hostname}_gpsData_{timestr}{gps_timestamp}.csv'
            f = open(gpsPath,'a+')
            print('NEW GPS FILE')

    except KeyboardInterrupt:
        f.close()
        print('\n Done Writing \n')
    except:
        print('ERROR')
        pass
    
    


if __name__ == '__main__':
    GPS()
