import time, csv, board, busio
import adafruit_mcp4728
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

R_SHUNT = 216.0
i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4728.MCP4728(i2c)
dac.channel_a.vref = adafruit_mcp4728.Vref.VDD
ads = ADS1115(i2c)
a0 = AnalogIn(ads, ads1x15.Pin.A0)
a1 = AnalogIn(ads, ads1x15.Pin.A1)

def avg(ch, gain, n=10):
    ads.gain = gain
    return sum(ch.voltage for _ in range(n)) / n

with open("golden_996.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["code", "v_top", "v_shunt", "v_dut", "i_ma", "r_calc"])
    for code in range(256, 4096, 256):
        dac.channel_a.raw_value = code
        time.sleep(0.05)
        v_top = avg(a0, 1)
        v_sh = avg(a1, 4)
        i = v_sh / R_SHUNT
        v_dut = v_top - v_sh
        r = v_dut / i if i > 0 else 0
        w.writerow([code, f"{v_top:.5f}", f"{v_sh:.5f}", f"{v_dut:.5f}", f"{i*1000:.4f}", f"{r:.1f}"])
        print(f"code {code:4d}  V_dut {v_dut:.4f} V  I {i*1000:.3f} mA  R {r:.1f} ohm")

dac.channel_a.raw_value = 0
