import sys, board, busio, adafruit_mcp4728
dac = adafruit_mcp4728.MCP4728(busio.I2C(board.SCL, board.SDA))
dac.channel_a.vref = adafruit_mcp4728.Vref.VDD
dac.channel_a.raw_value = int(sys.argv[1])
print("DAC set to", sys.argv[1])
