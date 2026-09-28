import statistics, board, busio
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)
chan = AnalogIn(ads, ads1x15.Pin.A0)

readings = [chan.voltage for _ in range(200)]
print(f"Mean: {statistics.mean(readings):.5f} V")
print(f"Std dev: {statistics.stdev(readings)*1000:.3f} mV")
