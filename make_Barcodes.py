#!/usr/bin/env python3
import barcode
from barcode.writer import ImageWriter

# Generate Note barcodes
notes = [
    "A",
    "A#",
    "B",
    "C",
    "C#",
    "D",
    "D",
    "E",
    "E#",
    "F",
    "F#",
    "G",
    "G#"
]

# Define smaller barcode settings
writer_options = {
    'module_width': 0.20,  # default is 0.2 
    'module_height': 3.0,  # default is 15.0
    'font_size': 3,        # default is 10
    'text_distance': 4.0,  # space between barcode and text
    'quiet_zone': 2.0,     # whitespace on sides
    'write_text': True     # include text under barcode
}

# Use Code128 format
code128 = barcode.get_barcode_class('code128')

# Generate and save each barcode
for note in notes:

    full_text = f"{note}"
    filename = f"{note}"
    code = code128(full_text, writer=ImageWriter())
    code.save(filename,options=writer_options) # adds the png extension
    #code.save(filename)
    print(f"Saved barcode: {filename}")

# write a latex output or out to a PDF!
