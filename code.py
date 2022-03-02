import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import usb_midi
import simpleio
import adafruit_midi
from adafruit_midi.control_change import ControlChange

class Fader():
    def __init__(self, mcp, pin, touchSensorPin, controlID):
        self.input = AnalogIn(mcp,pin)
        self.state = 0
        self.touchSensor = digitalio.DigitalInOut(touchSensorPin)
        self.ControlID = controlID
    @property
    def value(self):
        return self.input.value
    @property
    def savedValue(self):
        return self.state
    @savedValue.setter
    def savedValue(self, value):
        self.state = value
    @property
    def touch(self):
        return self.touchSensor.value
    @property
    def controlID(self):
        return self.ControlID
    @controlID.setter
    def controlID(self,value):
        self.ControlID = value

spi = busio.SPI(clock=board.GP2, MISO=board.GP4, MOSI=board.GP3)
cs = digitalio.DigitalInOut(board.GP26)
mcp = MCP.MCP3008(spi, cs)

faders = []
faders.append(Fader(mcp,MCP.P0,board.GP27,1))
midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], in_channel=0,midi_out=usb_midi.ports[1], out_channel=0 )



while True:
    for fader in faders:
        print(midi.receive())
        midi.send(ControlChange(fader.controlID,int(round(simpleio.map_range(fader.value, 0, 65472, 0, 127)))))
        #print('Raw ADC Value: ', fader.value)
        #if fader.value > fader.savedValue and not fader.touch:
        #    print(fader.value - fader.savedValue)
        #    fader.savedValue += 1
        #elif fader.value < fader.savedValue and not fader.touch:
        #    print(fader.savedValue - fader.value)
        #    fader.savedValue -= 1
        #else:
        #    pass
