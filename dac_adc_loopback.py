import time, csv, board, busio
import adafruit_mcp4728
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4728.MCP4728(i2c)
ads = ADS1115(i2c)
adc = AnalogIn(ads, ads1x15.Pin.A0)

dac.channel_a.vref = adafruit_mcp4728.Vref.VDD

with open("loopback.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["code", "expected_v", "adc_v"])
    for code in range(0, 4096, 128):
        dac.channel_a.raw_value = code
        time.sleep(0.05)
        v = sum(adc.voltage for _ in range(20)) / 20
        expected = code / 4096 * 3.3
        w.writerow([code, f"{expected:.4f}", f"{v:.5f}"])
        print(f"code {code:4d}  expected {expected:.3f} V  measured {v:.4f} V")
