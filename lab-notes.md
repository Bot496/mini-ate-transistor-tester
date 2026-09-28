# Lab Notes

## 2026-09-28: ADS1115 first measurements
- Setup: ADS1115 powered from Pi 3.3V, A0 to 3.3V rail
- Result: A0 = 3.29 V, noise (std dev) = 0.136 mV over 200 readings
- a noise level of ~1 LSB ("least significant bit", the smallest step the ADC can measure).
- Issue: A0 read ~0.9 V at first. Wire was on ALRT, not A0. A floating input reads a random value.
- Next: measure 0 V, compare against multimeter when it arrives
