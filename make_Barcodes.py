#!/usr/bin/env python3
import barcode
from barcode.writer import ImageWriter
import os

# Directory to save output
output_dir = "barcodes"
os.makedirs(output_dir, exist_ok=True)

# Define the musical riff (ordered)
riff = [
    "C", "C#", "D",
    "D#", "E", "F",
    "F", "G", "G#",
    "A", "A#", "B"
]

# Define barcode settings
writer_options = {
    'module_width': 0.18,
    'module_height': 1.5,
    'font_size': 3,
    'text_distance': 1.0,
    'quiet_zone': 1.0,
    'write_text': False
}

# Use Code128 barcode
code128 = barcode.get_barcode_class('code128')

# Track image filenames in order
image_files = []

for i, note in enumerate(riff):
    safe_note = note.replace("#", "s").replace("b", "b")  # avoid filename issues
    filename = f"{output_dir}/{i:02d}_{safe_note}"
    code = code128(note, writer=ImageWriter())
    filepath = code.save(filename, options=writer_options)
    image_files.append(os.path.basename(filepath))

    print(f"Saved barcode: {filepath}")

# Generate LaTeX document
latex_path = os.path.join(output_dir, "riff_barcodes.tex")

with open(latex_path, "w") as f:
    f.write(r"""
\documentclass[9pt]{article}
\usepackage{graphicx}
\usepackage[margin=0.5in]{geometry}
\pagestyle{empty}
\begin{document}
""")

    for img in image_files:
        f.write(f"\\includegraphics[width=0.65\\linewidth]{{{img}}}\\\\[0.5em]\n")

    f.write(r"\end{document}")
