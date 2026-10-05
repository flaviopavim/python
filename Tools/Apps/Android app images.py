#!/usr/bin/env python3
"""
Gera automaticamente:
- Ícones Android (mipmap-*)
- Imagens para publicação na Google Play Store

Requer:
    pip install pillow numpy
"""

import os

import numpy as np
from PIL import Image


# ============================================================
# CONFIGURAÇÕES
# ============================================================

# Imagem de origem.
# O arquivo deve estar na mesma pasta deste script.
SOURCE_IMAGE = "logo.png"

# Pasta onde os ícones Android serão gerados.
ANDROID_OUTPUT = "android-icons"

# Pasta onde as imagens da Play Store serão geradas.
PLAYSTORE_OUTPUT = "playstore-images"

# Cor de fundo utilizada quando a imagem possui transparência.
#
# Informe a cor em hexadecimal.
#
# Exemplos:
#   "#FFFFFF" = branco
#   "#000000" = preto
#   "#FF0000" = vermelho
#   "#F5F5F5" = cinza claro
BACKGROUND_COLOR = "#FFFFFF"

# Espaço em volta da imagem para as imagens da Play Store.
#
# 0  = imagem ocupa o máximo possível
# 10 = 10% de margem em cada lado
# 20 = 20% de margem em cada lado
PLAYSTORE_PADDING = 0

# ============================================================
# TAMANHOS DOS ÍCONES ANDROID
# ============================================================

ANDROID_SIZES = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

# ============================================================
# TAMANHOS DAS IMAGENS DA PLAY STORE
# ============================================================

PLAYSTORE_SIZES = [
    (512, 512),
    (607, 1080),
    (1024, 500),
    (1080, 527),
    (1080, 607),
    (4316, 7680),
]

# ============================================================
# CAMINHOS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SOURCE_PATH = os.path.join(BASE_DIR, SOURCE_IMAGE)
ANDROID_OUTPUT_PATH = os.path.join(BASE_DIR, ANDROID_OUTPUT)
PLAYSTORE_OUTPUT_PATH = os.path.join(BASE_DIR, PLAYSTORE_OUTPUT)


# ============================================================
# FUNÇÕES
# ============================================================

def hex_to_rgb(hex_color: str):
    """Converte uma cor hexadecimal para RGB."""
    hex_color = hex_color.strip().lstrip("#")

    if len(hex_color) != 6:
        raise ValueError(
            "BACKGROUND_COLOR deve estar no formato hexadecimal #RRGGBB."
        )

    try:
        return tuple(
            int(hex_color[index:index + 2], 16)
            for index in (0, 2, 4)
        )
    except ValueError as error:
        raise ValueError(
            "BACKGROUND_COLOR contém uma cor hexadecimal inválida."
        ) from error


def has_transparency(image: Image.Image):
    """Verifica se a imagem possui pixels transparentes."""
    if "A" not in image.getbands():
        return False

    alpha = image.getchannel("A")

    # Verifica se existe pelo menos um pixel com transparência.
    minimum_alpha = alpha.getextrema()[0]

    return minimum_alpha < 255


def get_border_color(image: Image.Image):
    """Obtém a cor de fundo através da mediana dos pixels das bordas."""
    rgb = np.asarray(image.convert("RGB"))

    edges = np.concatenate([
        rgb[0],
        rgb[-1],
        rgb[:, 0],
        rgb[:, -1],
    ])

    return tuple(
        int(value)
        for value in np.median(edges, axis=0)
    )


def get_background_color(image: Image.Image):
    """
    Obtém a cor de fundo da imagem.

    Se a imagem possuir transparência:
        usa BACKGROUND_COLOR.

    Se não possuir transparência:
        usa a cor calculada pelas bordas.
    """
    if has_transparency(image):
        return hex_to_rgb(BACKGROUND_COLOR)

    return get_border_color(image)


def flatten_image(image: Image.Image, background_color):
    """Remove a transparência colocando a imagem sobre o fundo definido."""
    background = Image.new(
        "RGBA",
        image.size,
        background_color + (255,),
    )

    background.alpha_composite(image)

    return background.convert("RGB")


def crop_center_square(image: Image.Image):
    """Recorta o maior quadrado possível a partir do centro da imagem."""
    width, height = image.size
    size = min(width, height)

    left = (width - size) // 2
    top = (height - size) // 2

    return image.crop((
        left,
        top,
        left + size,
        top + size,
    ))


def generate_android_icons(image: Image.Image):
    """Gera todos os tamanhos de ícones Android."""
    print()
    print("=" * 60)
    print("GERANDO ÍCONES ANDROID")
    print("=" * 60)

    # Para os ícones Android, usamos apenas o quadrado central.
    square = crop_center_square(image)

    os.makedirs(ANDROID_OUTPUT_PATH, exist_ok=True)

    for folder, size in ANDROID_SIZES.items():
        output_folder = os.path.join(
            ANDROID_OUTPUT_PATH,
            folder,
        )

        os.makedirs(output_folder, exist_ok=True)

        resized = square.resize(
            (size, size),
            Image.LANCZOS,
        )

        output_path = os.path.join(
            output_folder,
            "ic_launcher.png",
        )

        resized.save(
            output_path,
            "PNG",
            optimize=True,
        )

        print(
            f"✓ {folder}/ic_launcher.png ({size}x{size})"
        )


def generate_playstore_images(
    image: Image.Image,
    background_color,
):
    """Gera todas as imagens nos tamanhos definidos para a Play Store."""
    print()
    print("=" * 60)
    print("GERANDO IMAGENS DA PLAY STORE")
    print("=" * 60)

    # Remove a transparência utilizando a cor de fundo definida.
    image = flatten_image(
        image,
        background_color,
    )

    os.makedirs(
        PLAYSTORE_OUTPUT_PATH,
        exist_ok=True,
    )

    for width, height in PLAYSTORE_SIZES:
        padding = round(
            min(width, height) * PLAYSTORE_PADDING / 100
        )

        box_width = max(
            1,
            width - 2 * padding,
        )

        box_height = max(
            1,
            height - 2 * padding,
        )

        # Calcula a escala para manter a proporção original.
        scale = min(
            box_width / image.width,
            box_height / image.height,
        )

        new_width = max(
            1,
            round(image.width * scale),
        )

        new_height = max(
            1,
            round(image.height * scale),
        )

        resized = image.resize(
            (new_width, new_height),
            Image.LANCZOS,
        )

        # Cria a imagem final com o tamanho solicitado.
        canvas = Image.new(
            "RGB",
            (width, height),
            background_color,
        )

        # Centraliza a imagem.
        x = (width - new_width) // 2
        y = (height - new_height) // 2

        canvas.paste(
            resized,
            (x, y),
        )

        output_path = os.path.join(
            PLAYSTORE_OUTPUT_PATH,
            f"{width}x{height}.png",
        )

        canvas.save(
            output_path,
            "PNG",
            optimize=True,
        )

        print(
            f"✓ {PLAYSTORE_OUTPUT}/{width}x{height}.png"
        )


def main():
    """Executa a geração completa."""
    print("=" * 60)
    print("GERADOR DE IMAGENS")
    print("=" * 60)

    print(f"Imagem: {SOURCE_IMAGE}")
    print(f"Cor de transparência: {BACKGROUND_COLOR}")
    print(f"Padding Play Store: {PLAYSTORE_PADDING}%")

    # Verifica se a imagem existe antes de iniciar.
    if not os.path.isfile(SOURCE_PATH):
        print()
        print("ERRO: imagem não encontrada:")
        print(SOURCE_PATH)
        print()
        return

    # Valida a cor configurada antes de processar a imagem.
    try:
        configured_background = hex_to_rgb(
            BACKGROUND_COLOR
        )
    except ValueError as error:
        print()
        print(f"ERRO: {error}")
        print()
        return

    try:
        image = Image.open(SOURCE_PATH).convert("RGBA")
    except Exception as error:
        print()
        print("ERRO ao abrir a imagem:")
        print(error)
        print()
        return

    print(
        f"Dimensões originais: "
        f"{image.width}x{image.height}"
    )

    # Define automaticamente a cor de fundo.
    #
    # Imagem transparente:
    #   usa BACKGROUND_COLOR.
    #
    # Imagem sem transparência:
    #   usa a cor das bordas.
    background_color = get_background_color(image)

    print(
        "Fundo utilizado: "
        f"#{background_color[0]:02X}"
        f"{background_color[1]:02X}"
        f"{background_color[2]:02X}"
    )

    # Gera os dois conjuntos de imagens.
    generate_android_icons(image)
    generate_playstore_images(
        image,
        background_color,
    )

    print()
    print("=" * 60)
    print("CONCLUÍDO")
    print("=" * 60)
    print()
    print(
        f"Ícones Android: "
        f"{ANDROID_OUTPUT_PATH}"
    )
    print(
        f"Play Store:     "
        f"{PLAYSTORE_OUTPUT_PATH}"
    )
    print()


if __name__ == "__main__":
    main()
