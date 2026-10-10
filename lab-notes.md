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
