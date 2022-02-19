from time import time
from time import sleep

import board
import busio

import adafruit_gps
import adafruit_lsm303_accel
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1x15 import Mode
import adafruit_ads1x15.ads1015 as ADS

import serial

i2c = busio.I2C(board.SCL, board.SDA, frequency = 1000000)

try:
    ads = ADS.ADS1015(i2c, data_rate = 3300, gain = 2/3)
    ads.mode = Mode.CONTINUOUS

    chan = AnalogIn(ads, ADS.P0, ADS.P1)
    x = [time(), chan.voltage]
    print('ADC Connected')
except:
    print('Error in ADC Connection...')


try:
    accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
    x = [time(), accel.acceleration[0], accel.acceleration[1], accel.acceleration[2]]
    print('IMU Connected')
except:
    print('Error in IMU Connection...')

try:
    uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
    gps = adafruit_gps.GPS(uart, debug=False) # Use UART/pyserial

    # Turn on the basic GGA and RMC info (what you typically want)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

    # Set update rate to once a second (1hz) which is what you typically want.
    gps.send_command(b"PMTK220,1000")

    for i in range(10):
        gps.update()
        if gps.has_fix:
            x = [time(), gps.latitude, gps.longitude, gps.speed_knots, gps.fix_quality, gps.satellites]
            print('GPS Connected')
            break
        sleep(1)
    if i == 9:
        print('Error in GPS Connection...')
except:
    print('Error in GPS Connection...')

print('All Sensors Tested')
