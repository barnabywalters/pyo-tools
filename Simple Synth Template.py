from pyo import *

# Set Up Server
s = Server()
s.setMidiInputDevice(2)
s.boot()
s.start()

# Set Up MIDI
midi = Notein()

# ADSR
amp = MidiAdsr(midi['velocity'])

# Pitch
pitch = MToF(midi['pitch'])

# Table
wave = SquareTable()
wave.view()

# Osc
osc = Osc(wave, freq=pitch, mul=amp)

# FX
verb = Freeverb(osc).out()

### Go
osc.out()
s.gui(locals())