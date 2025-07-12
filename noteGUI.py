#!/usr/bin/env python3
import threading

import simpleaudio as sa
import numpy as np
import tkinter as tk
from tkinter import ttk
# sudo apt-get install -y python3-dev libasound2-dev
# https://simpleaudio.readthedocs.io/en/latest/installation.html#linux-dependencies
# manual: https://prod-edam.honeywell.com/content/dam/honeywell-edam/sps/ppr/ja/public/products/barcode-scanners/general-purpose-handheld/1300g/documents/sps-ppr-hp1300-ug.pdf?download=false
notes = {
    "C": 261.63, "C#": 277.18, "D": 293.66, "D#": 311.13,
    "E": 329.63, "F": 349.23, "F#": 369.99, "G": 392.00,
    "G#": 415.30, "A": 440.00, "A#": 466.16, "B": 493.88
}

buffer = ""

def play_note(freq):

    duration = duration_slider.get()
    fs = 44100
    t = np.linspace(0, duration, int(fs * duration), True)
    pitch = pitch_slider.get()
    vol = vol_slider.get() / 100.0
    ch = int(ch_slider.get())
    bps = int(bp_slider.get())
    N = 2
    freq *= pitch / octave_slider.get()
    decay_rate = decay_slider.get()
    envelope = np.exp(-decay_rate * t)
    #harmonics = [1, 2, 3, 4]  # multiples of base freq
    #wave = sum(0.5 / N * np.sin(2 * np.pi * freq * N * t) for n in harmonics)
    wave = 0.5 * np.sin(N * np.pi * freq * t) * envelope
    #wave = 0.5 * np.sin(2 * np.pi * freq * t)
    wave = wave * (vol * 32767)
    audio = wave.astype(np.int16)

    if ch == 2:
        wave1 = 0.5 * np.tan(N * np.pi * freq * t) * envelope
        #wave = 0.5 * np.sin(2 * np.pi * freq * t)
        wave1 = wave1 * (vol * 32767)
        audio1 = wave1.astype(np.int16)
        audio1 = np.column_stack((audio, audio1)).flatten()

    #sa.play_buffer(audio, ch, bps, fs).wait_done()
    threading.Thread(target=lambda: sa.play_buffer(audio, ch, bps, fs).wait_done(), daemon=True).start()
def on_key(event):
    global buffer
    char = event.char.upper()

    if event.keysym == "Return":
        note = buffer.strip()
        if note in notes:
            play_note(notes[note])
            status.set(f"Played: {note}")
        else:
            status.set(f"Unknown: {note}")
        buffer = ""  # Clear for next scan
    elif char.isalnum() or char in "#":
        buffer += char

# === GUI ===
root = tk.Tk()
root.title("Note Player (Barcode Ready)")

main = ttk.Frame(root, padding=10)
main.grid()

# Volume
ttk.Label(main, text="Volume (%)").grid(column=0, row=0, sticky="w")
vol_slider = ttk.Scale(main, from_=0, to=100, orient="horizontal")
vol_slider.set(50)
vol_slider.grid(column=1, row=0, columnspan=2, sticky="ew")

# Channels
ttk.Label(main, text="Channels (1=Mono, 2=Stereo)").grid(column=0, row=1, sticky="w")
ch_slider = tk.Scale(main, from_=1, to=2, resolution=1, orient="horizontal")
ch_slider.set(1)
ch_slider.grid(column=1, row=1, columnspan=2, sticky="ew")

# Bits per sample
ttk.Label(main, text="Bits per Sample (1–4)").grid(column=0, row=2, sticky="w")
bp_slider = tk.Scale(main, from_=1, to=4, resolution=1, orient="horizontal")
bp_slider.set(2)
bp_slider.grid(column=1, row=2, columnspan=2, sticky="ew")

# Pitch bend
ttk.Label(main, text="Pitch Bend (0.5–2.0)").grid(column=0, row=3, sticky="w")
pitch_slider = tk.Scale(main, from_=0.25, to=2.0, resolution=0.25, digits=4, orient="horizontal", length=200)
pitch_slider.set(1.0)
pitch_slider.grid(column=1, row=3, columnspan=2, sticky="ew")

# Octave
ttk.Label(main, text="Octave (0.25–2.0)").grid(column=0, row=4, sticky="w")
octave_slider = tk.Scale(main, from_=0.25, to=2.0, resolution=0.25, digits=4, orient="horizontal", length=200)
octave_slider.set(1.0)
octave_slider.grid(column=1, row=4, columnspan=2, sticky="ew")

# Duration
ttk.Label(main, text="Duration (0.1–2.5)").grid(column=0, row=5, sticky="w")
duration_slider = tk.Scale(main, from_=0.1, to=2.5, resolution=0.01, digits=4, orient="horizontal", length=200)
duration_slider.set(0.3)
duration_slider.grid(column=1, row=5, columnspan=2, sticky="ew")

# Decay 
ttk.Label(main, text="Decay Rate (1–20)").grid(column=0, row=6, sticky="w")
decay_slider = tk.Scale(main, from_=1, to=20, resolution=0.1, orient="horizontal", length=200)
decay_slider.set(5)
decay_slider.grid(column=1, row=6, columnspan=2, sticky="ew")

# Status
status = tk.StringVar()
ttk.Label(main, textvariable=status, foreground="blue").grid(column=0, row=7, columnspan=3, sticky="w")

main.columnconfigure(1, weight=1)

# Bind keys globally
root.bind_all("<Key>", on_key)

root.mainloop()

''' Todo:
The actual goal here is to convert the barcode scanner to a wand, and have the settings change based on depth data from the xbox 360 kinect.
Figuring out settings that make sense is easier with a GUI. 

'''

