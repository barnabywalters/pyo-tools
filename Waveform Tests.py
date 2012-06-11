from pyo import *

# Set Up Server
s = Server(audio='pa', duplex=1)
s.setMidiInputDevice(2) # Change as required
s.boot()
s.start()

# Set Up MIDI
midi = Notein()
m = Midictl(ctlnumber=1, minscale=0, maxscale=1) # mod wheel
bend = Bendin(brange=2, scale=1)
cutoff = Midictl(ctlnumber=28, minscale=0, maxscale=15000) # cutoff knob
drive = Midictl(ctlnumber=31, minscale=0, maxscale=1) # drive knob
rate = Midictl(ctlnumber=90, minscale=0, maxscale=10) # lfo rate
amount = Midictl(ctlnumber=70, minscale=0, maxscale=10000) # lfo amount

# ADSR
amp = MidiAdsr(midi['velocity'])

# Pitch
pitch = MToF(midi['pitch'])

# Table
wave1 = DataTable(1)
wave1.read(os.path.expanduser('./waveforms/create_met_temp_curve_table.txt'))
wave1.normalize()

wave2 = SquareTable()

wave3 = NewTable(length=8192/s.getSamplingRate(), chnls=1)

morph = TableMorph(input=m, table=wave3, sources=[wave1, wave2])

# LFO
lfo = LFO(freq=rate, type=3, mul=1) # ^^^

# Osc
osc = Osc(wave3, freq=pitch * bend, mul=amp*0.5)
# - LP Filter
lp = Biquad(osc, freq=cutoff - (lfo * amount), type=0) # TODO: Make amount control work properly

# FX
disto = Disto(lp, drive=drive).out()
delay = Delay(disto, delay=0.4, feedback=0.5, mul=0.5)
verb = WGVerb(delay).out()

### Go
lp.out()
s.gui(locals()) # Prevents immediate script termination.






