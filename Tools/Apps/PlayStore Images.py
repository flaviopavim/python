#!/usr/bin/env python3
"""Gera imagens para a publicação na Play Store a partir de uma imagem.

- Não recorta: a imagem é redimensionada para caber e centralizada.
- O fundo é preenchido com a cor das bordas da imagem original.
- PADDING define o espaço em volta da imagem.

Requer: pip install pillow numpy
"""
import os

import numpy as np
from PIL import Image

# ---------------- CONFIG ----------------
SRC = "logo.png"   # imagem de origem (mesma pasta do script)
OUT = "playstore-images"       # pasta de saída

# Espaço em volta da imagem, em % do menor lado de cada tamanho final.
# 0 = encosta nas bordas; 10 = 10% de margem em cada lado.
PADDING = 0

SIZES = [
    (512, 512),
    (607, 1080),
    (1024, 500),
    (1080, 527),
    (1080, 607),
    (4316, 7680),
]
# ----------------------------------------

BASE = os.path.dirname(os.path.abspath(__file__))


def border_color(img: Image.Image):
    """Cor de fundo = mediana dos pixels da borda da imagem."""
    a = np.asarray(img.convert("RGB"))
    edge = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    return tuple(int(v) for v in np.median(edge, axis=0))


def main():
    img = Image.open(os.path.join(BASE, SRC)).convert("RGBA")
    bg = border_color(img)

    # achata transparência sobre a cor de fundo
    flat = Image.new("RGBA", img.size, bg + (255,))
    flat.alpha_composite(img)
    img = flat.convert("RGB")

    out_dir = os.path.join(BASE, OUT)
    os.makedirs(out_dir, exist_ok=True)

    for w, h in SIZES:
        pad = round(min(w, h) * PADDING / 100)
        box_w, box_h = max(1, w - 2 * pad), max(1, h - 2 * pad)

        scale = min(box_w / img.width, box_h / img.height)
        nw, nh = max(1, round(img.width * scale)), max(1, round(img.height * scale))
        resized = img.resize((nw, nh), Image.LANCZOS)

        canvas = Image.new("RGB", (w, h), bg)
        canvas.paste(resized, ((w - nw) // 2, (h - nh) // 2))
        canvas.save(os.path.join(out_dir, f"{w}x{h}.png"), "PNG", optimize=True)
        print(f"{OUT}/{w}x{h}.png")


if __name__ == "__main__":
    main()