#!/usr/bin/env python3
import simpleaudio as sa
import numpy as np

'''
# honeywell 1300g-2-06211
manual: https://prod-edam.honeywell.com/content/dam/honeywell-edam/sps/ppr/ja/public/products/barcode-scanners/general-purpose-handheld/1300g/documents/sps-ppr-hp1300-ug.pdf?download=false
page 45 turns off beep sound
'''

notes = {
    "C": 261.63,
    "C#": 277.18,
    "D": 293.66,
    "D#": 311.13,
    "E": 329.63,
    "F": 349.23,
    "F#": 369.99,
    "G": 392.00,
    "G#": 415.30,
    "A": 440.00,
    "A#": 466.16,
    "B": 493.88
}

def play_note(freq, duration=0.3):
    
    #numpy trig functions: cos sin tan arctan arcsin arccos

    fs = 44100  # sampling rate: "Weird sample rates are not supported."
    vol = 32767 # volume
    bpS = 4     # bits per Sample 1-4
    ch = 1      # channels
    t = np.linspace(0, duration, int(fs * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * freq * t)
    audio = (wave * vol).astype(np.int16)
    sa.play_buffer(audio, ch, bpS, fs).wait_done()

print("Scan a note (C, D#, F#, etc.):")
try:
    while True:
        scanned = input().strip().upper()
        if scanned in notes:
            play_note(notes[scanned])
        else:
            print(f"Unknown note: {scanned}")
except KeyboardInterrupt:
    print("Exiting.")

''' row your boat
C   C   C   D   E
E   D   E   F   G
C   C   C   G   G
G   E   E   E   C
C   C   D   E   F
E   C   G   G   C

'''

'''
next episode Dr Dre
G   B   C   G   
B   C   G   B  
C   G   B   C

'''
