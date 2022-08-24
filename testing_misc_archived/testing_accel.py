import board
import busio
import adafruit_adxl34x
import time

i2c = busio.I2C(board.SCL, board.SDA)
accel = adafruit_adxl34x.ADXL345(address=0x53, i2c=i2c)
while True:
	print("%f %f %f"%accel.acceleration)
	time.sleep(1)
