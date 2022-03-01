from machine import Pin, SPI
from mcp3008 import MCP3008


spi = SPI(0, sck=Pin(2),mosi=Pin(3),miso=Pin(4), baudrate=100000)
cs = Pin(26, Pin.OUT)
cs.value(1) # disable chip at start
chip = MCP3008(spi, cs)

while True:
    print(chip.read(0))