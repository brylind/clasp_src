import board
import adafruit_adxl34x
from time import time
import busio

def main():

	i2c = busio.I2C(board.SCL, board.SDA)
	accel = adafruit_adxl34x.ADXL345(address=0x53, i2c=i2c)
	accel.DataRate=3200
	s = 20	# seconds of recording

	start = time()

	while (time()-start) < s:
		print(accel.acceleration[1])


main()
