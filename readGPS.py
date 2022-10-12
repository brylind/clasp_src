# Author: Bryce Lindsey (bryce.lindsey@okstate.edu)
# Date: April 1 2022
# Description: Script that records GPS data on GLINDA 2.0
# ##############################################################################
# ##############################################################################
# ~~~~~~~~~~~~~~~~~~ DETAILED COMMENTS ~~~~~~~~~~~~~~~~~~
# i) The update rate is somewhat irrelevant for this project, as GPS data isn't terribly crucial.
# However, what is important is that when acquiring GPS data, make sure the update() method is
# called AT LEAST twice per update period. For example, if the GPS module update rate is set to
# 10000 (once every 10 seconds), you need to call "gps.update()" at least once every 5 seconds.
# If not, the buffer will fill faster than you're emptying it and the GPS data will be
# continuously written at a time earlier than you intend.
# ii) Sleep for 4 seconds to provide a small overlap between data updated and data written.
# This way, data will be written 2.5 times (10/4) per GPS update (see D.C. "i")
# iii) The length of each GPS file will be:
# sleep value x i full range x j full range. As of 4/27/2022, for example, the loop sleeps
# for 4 seconds each iteration, i goes to 15, j goes to 5... so each file will be 300
# seconds long
#
# RTC on the GPS module:
# The Adafruit GPS Breakout has RTC capabilities, but it's not accessible. It is useful, though,
# because after the first "fix" the GPS module will maintain time through its RTC (as long as a
# proper battery is installed on the breakout).
# This serves as a good sanity check in this script (comparing GPS time to the system time on the Pi)


# ##############################################################################
def GPS():
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ import the goodies ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    from time import sleep, time
    import adafruit_gps
    import datetime
    import board
    import busio
    import socket
    import serial
    import urllib.request
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ SUPPORTING NESTED FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def check_internet():
        try:
            _ = urllib.request.urlopen('https://www.google.com', None, timeout=5.1)
            print('GOOGLE reached (there is internet)')
            return True
        except:
            print(f'no internet')
            return False

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    device_hostname = socket.gethostname()  # hostname is used for data storage
    uart = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=100)
    gps = adafruit_gps.GPS(uart, debug=False)  # define GPS object

    # Turn on the basic GGA and RMC NMEA info (what you typically want)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

    # --> DETAILED COMMENT "i"
    gps.send_command(b"PMTK220,10000")  # set the update rate to once every 10 seconds

    if check_internet():    # check for network status
        internet = ''
    else:
        internet = 'NOINT_'

    launch_time = datetime.datetime.now()
    timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")
    gpsPath = f'/home/pi/glinda_main/dataFiles/gps/{internet}{device_hostname}_gpsData_{timestr}.csv'
    f = open(gpsPath, 'a+')
    dat = []

    try:
        while 1:
            f.write('Time_s' + ',' + 'Latitude' + ',' + 'Longitude' + ',' + 'Speed_kts' + ',' + 'GPS_fix' +
                    ',' + 'Satellites' + ',' + 'GPS_UTCtime_H_M_S' + '\n')
            # --> DETAILED COMMENT "iii"
            for j in range(5):
                for i in range(15):
                    gps.update()
                    if gps.has_fix:  # gps fix: 0=no, 1=yes, 2=differential fix
                        gps_time = (
                            f'{gps.timestamp_utc.tm_hour}_{gps.timestamp_utc.tm_min}_{gps.timestamp_utc.tm_sec}')
                        dat.append(
                            [time(), gps.latitude, gps.longitude, gps.speed_knots, gps.fix_quality,
                             gps.satellites, gps_time])
                    else:
                        dat.append([time(), 0, 0, -1, -1, 0, 0])
                    # --> DETAILED COMMENT "ii"
                    sleep(4)

                for d in dat:
                    f.write(str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) + ',' +
                            str(d[3]) + ',' + str(d[4]) + ',' + str(d[5]) + ',' + str(d[6]) + '\n')
                dat = []  # help clear out ram so "dat" can be refilled with data
            f.close()

            if check_internet():
                internet = ''
            else:
                internet = 'NOINT_'
            launch_time = datetime.datetime.now()
            timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")
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
