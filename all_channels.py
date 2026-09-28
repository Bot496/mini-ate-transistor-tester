import board, busio
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)

for name in ["A0", "A1", "A2", "A3"]:
    chan = AnalogIn(ads, getattr(ads1x15.Pin, name))
    print(f"{name}: {chan.voltage:.4f} V")
