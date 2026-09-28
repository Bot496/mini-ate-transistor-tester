# Lab Notes: Mini ATE Transistor Tester

## 2026-09-28: ADS1115 bring-up and first measurements

### Setup
- Raspberry Pi 4 Model B, powered from laptop USB
- ADS1115 16-bit ADC, connected via I2C (address 0x48)
- Wiring: VDD to Pi 3.3V (pin 1), GND and ADDR to ground, SDA to pin 3, SCL to pin 5
- Default settings: gain = 1 (±4.096 V range), 1 LSB = 0.125 mV
- 200 readings per measurement

### Results
| Input | Mean | Noise (std dev) |
|---|---|---|
| A0 to 3.3V rail | 3.29404 V | 0.136 mV (~1 LSB) |
| A0 to ground | -0.00011 V | 0.038 mV |

- Offset error at 0 V: -0.11 mV (~1 LSB)
- Noise is lower at 0 V than at 3.3 V, since reference noise scales with input voltage
- Noise at 3.3 V is about 1 LSB, so the setup is close to the ADC's resolution limit

### Issues and fixes
- A0 read ~0.9 V on all channels at first, despite being "connected"
- Cause: wire was attached to the ALRT pin instead of A0, so A0 was floating
- Floating inputs read a random, meaningless value; always check a known 0 V and 3.3 V reference when bringing up a new measurement

### To do
- Repeatability: run 10 times at 3.3 V and record variation in the mean
- Power check: record `vcgencmd get_throttled` result
- Compare against a multimeter to find absolute accuracy error
- Speed vs. noise experiment across ADS1115 data rates# Lab Notes

## 2026-09-28: ADS1115 first measurements
- Setup: ADS1115 powered from Pi 3.3V, A0 to 3.3V rail
- Result: A0 = 3.29 V, noise (std dev) = 0.136 mV over 200 readings
- a noise level of ~1 LSB ("least significant bit", the smallest step the ADC can measure).
- Issue: A0 read ~0.9 V at first. Wire was on ALRT, not A0. A floating input reads a random value.
- Next: measure 0 V, compare against multimeter when it arrives
