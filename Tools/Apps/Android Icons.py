#!/usr/bin/env python3
"""Lê ic_launcher.png (na mesma pasta do script) e gera as pastas mipmap-*.

Requer: pip install pillow
"""
import os

from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "logo.png")
OUT = os.path.join(BASE, "android-icons")

SIZES = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

img = Image.open(SRC).convert("RGBA")

# recorta o quadrado central
w, h = img.size
s = min(w, h)
left, top = (w - s) // 2, (h - s) // 2
img = img.crop((left, top, left + s, top + s))

for folder, size in SIZES.items():
    d = os.path.join(OUT, folder)
    os.makedirs(d, exist_ok=True)
    img.resize((size, size), Image.LANCZOS).save(os.path.join(d, "ic_launcher.png"), "PNG", optimize=True)
    print(f"{folder}/ic_launcher.png ({size}x{size})")
