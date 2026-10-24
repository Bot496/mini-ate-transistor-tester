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

## 2026-10-10: Resistor measurements (multimeter)

### Setup
- Digital multimeter, resistance mode
- Each resistor measured alone on the breadboard (no other connections), probes on the resistor legs
- Ranges: 200 Ω range for 10 Ω (0.1 Ω resolution), 2k range for 220 Ω and 1 kΩ (1 Ω resolution)
- Probe lead resistance not subtracted

### Results
| Nominal | Readings | Deviation from nominal | Selected |
|---|---|---|---|
| 10 Ω | 10.3 Ω, 10.4 Ω, 10.1 Ω | +1.0% to 4.0% | not used |
| 220 Ω | 215 Ω, 216 Ω, 216 Ω | -2.3% to -1.8% | 216 Ω, current shunt |
| 1 kΩ | 981 Ω, 985 Ω, 996 Ω | -1.9% to -0.4% | 996 Ω, golden reference |

- 10 Ω readings are limited by meter accuracy (about ±0.3-0.5 Ω) and contact resistance, so only good to "about 10 Ω"
- Two matching 220 Ω readings (216 Ω) show the measurement is repeatable
- Most readings sit 1.5-2.3% below nominal; too few samples to tell meter offset from part-to-part variation

### Shunt decision
- No 100 Ω resistors on hand
- 1 kΩ rejected: drops 1 V at 1 mA, leaving too little voltage for the DUT
- 10 Ω rejected: value only known to ~4%, and 10 mV at 1 mA needs maximum ADC gain
- 220 Ω chosen: drops 0.22 V at 1 mA, leaving ~3.08 V for the DUT, and limits current to ~15 mA if a DUT shorts

### Issues and fixes
- Readings jumped erratically at first
- Cause: poor probe contact; holding the resistor in the breadboard and pressing probes on its legs gave stable readings
- Low resistances are hard to measure because lead and contact resistance add in; professional testers use Kelvin (4-wire) measurement

### To do
- Fill in remaining 10 Ω readings
- Confirm the 216 Ω shunt value with the golden test (996 Ω resistor)
- Parts with V_th close to 3 V may not reach 1 mA; report them as "no threshold found"

## 2026-10-11: MCP4728 DAC to ADS1115 loopback

### Setup
- MCP4728 12-bit DAC and ADS1115 16-bit ADC sharing the Pi's I2C bus (addresses 0x60 and 0x48)
- Both powered from the Pi 3.3V rail; DAC reference = VDD
- DAC channel A output (VA) wired to ADS1115 A0
- Swept DAC codes 0 to 3968 in steps of 128; 50 ms settling, 20 ADC readings averaged per step
- Script: dac_adc_loopback.py, data: loopback.csv

### Results
| DAC code | Expected (3.3 V ref) | Measured | Error |
|---|---|---|---|
| 0 | 0.000 V | 0.0011 V | +1.1 mV |
| 1024 | 0.825 V | 0.8226 V | -2.4 mV |
| 2048 | 1.650 V | 1.6424 V | -7.6 mV |
| 3072 | 2.475 V | 2.4647 V | -10.3 mV |
| 3968 | 3.197 V | 3.1815 V | -15.5 mV (-0.48%) |

- Offset error: +1.1 mV at code 0
- Gain error: about -0.5%, growing in proportion to the output voltage
- Linearity: error grows smoothly with no jumps, so the DAC and ADC respond linearly
- Part of the gain error comes from the supply: the rail is 3.294 V, not 3.3 V. Recalculating with 3.294 V, the error at code 3968 drops to about -9.6 mV (-0.30%)
- Remaining ~0.3% is the combined DAC and ADC error, within their datasheet specs

### Issues and fixes
- First run read a constant 0.908 V at every code
- Cause: only SDA and SCL were connected; the DAC's output pin (VA) was not wired to A0, so A0 was floating
- SDA/SCL carry commands only; the analog output comes from VA-VD
- Same 0.908 V floating value as the earlier ALRT mix-up, so a constant ~0.9 V reading is a reliable sign of an unconnected input

### To do
- Recalculate expected values using the measured 3.294 V supply
- Spot-check a few DAC codes with the multimeter on VA
- Add the MCP6022 buffer and rerun the loopback through it

## 2026-10-24: DAC spot-check with multimeter

### Setup
- DAC held at a fixed code with dac_hold.py
- Multimeter on DC volts, measuring VA to ground
- ADC values taken from the 2026-10-11 loopback (A0 wired to VA)
- Expected = code / 4096 x 3.294V (measured supply)

### Results
| Code | Expected | Multimeter | Meter range | ADC (loopback) |
|---|---|---|---|---|
| 512 | 0.412 V | 0.412 V | 2V | 0.410 V |
| 2048 | 1.647 V | 1.64 V | 2V | 1.64 V |
| 3584 | 2.882 V | 2.88 V | 20V | 2.876 V |

- DAC output matches expected within the meter's display resolution
- ADC reads about 2-4 mV below the meter, so most of the loopback gain error appears to come from the ADC side
- Limitation: meter accuracy is roughly +/-0.5% plus a few digits (about +/-15 mV at 2.88 V), larger than the differences being compared. Results are consistent with an accurate DAC and a slightly low ADC, but the meter cannot prove it
- A valid check needs a reference roughly 4-10x more accurate than the device under test (test accuracy ratio)

### Issues
- At code 2048, the 2V range display kept blanking, so it was measured on the 20V range (2 decimals only)
- Possible causes: reading too close to the range limit, or unstable probe contact. Not investigated further

### To do
- Add the MCP6022 buffer and rerun the loopback through it

## 2026-10-24: MCP6022 buffer
- Wired op-amp A as a voltage follower: VA to pin 3, pin 2 to pin 1, pin 1 to A0
- Unused op-amp B tied off (pin 5 to ground, pin 6 to pin 7); 0.1uF cap at pin 8
- Buffered loopback matches the unbuffered one within 0.4 mV at every code
- Difference is consistent with op-amp input offset voltage
- Output still covers 0.0014 V to 3.18 V, so rail-to-rail range is fine
- No load yet; buffer's benefit shows under load (next: golden test)

## 2026-10-24: Golden resistor test
- DUT: 995-996 ohm resistor (multimeter). Shunt: 216 ohm
- Tester result: about 997 ohm from 1 mA upward (within 0.2% of meter)
- At low current R reads higher (1003 ohm at 0.17 mA): small fixed offsets dominate small signals
- Confirms shunt value and measurement chain are correct
- Debugging: (1) A1 read 0 V - row X grounded, shunt bypassed. (2) A1 = A0 - shunt not connected, no current. (3) A1 stuck at 1.024 V - shunt on + rail instead of - rail
- Next: first 2N7000 threshold voltage
