#!/usr/bin/env python3
"""
Gera automaticamente:
- Ícones Android (mipmap-*)
- Imagens para publicação na Google Play Store
- Favicons para navegadores
- Ícones para dispositivos Apple
- Ícones iOS em formato AppIcon.appiconset
- Artes-base nos tamanhos comuns da App Store
- Ícones para aplicações PWA
- Ícones maskable para Android e PWA
- Imagens de compartilhamento para redes sociais
- SVG para abas fixadas do Safari
- Arquivos de configuração para PWA e Windows

Requer:
    pip install pillow numpy

Arquivo de origem:
    logo.png
"""

import json
import os
import struct

import numpy as np
from PIL import Image, ImageDraw


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

# Pasta onde os favicons e as imagens para sites serão gerados.
SITE_OUTPUT = "site-images"

# Pastas adicionais para publicação na App Store.
IOS_OUTPUT = "ios-icons"
APPSTORE_OUTPUT = "applestore-images"

# Cor de fundo utilizada quando a imagem possui transparência.
#
# Exemplos:
#   "#FFFFFF" = branco
#   "#000000" = preto
#   "#F5F5F5" = cinza claro
BACKGROUND_COLOR = "#FFFFFF"

# Espaço em volta da imagem para as imagens da Play Store.
#
# 0  = imagem ocupa o máximo possível
# 10 = 10% de margem em cada lado
# 20 = 20% de margem em cada lado
PLAYSTORE_PADDING = 0

# Espaço em volta da imagem para a miniatura de compartilhamento.
#
# Utiliza o mesmo padrão de padding das artes da Play Store,
# mas permite configurar um valor independente.
SHARE_PADDING = 0

# Cor de fundo da miniatura de compartilhamento.
#
# None utiliza automaticamente o fundo calculado para a logo.
SHARE_BACKGROUND_COLOR = None

# Nome utilizado nos metadados do manifesto PWA.
SITE_NAME = "Meu Site"
SITE_SHORT_NAME = "Meu Site"
SITE_DESCRIPTION = "Aplicação web"

# URL inicial do aplicativo PWA.
PWA_START_URL = "/"

# Cor do tema do navegador.
THEME_COLOR = "#FFFFFF"

# Cor de destaque para a aba fixada do Safari.
SAFARI_PINNED_COLOR = "#000000"

# Gera o arquivo browserconfig.xml para compatibilidade com Windows.
GENERATE_WINDOWS_CONFIG = True


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
# TAMANHOS DOS FAVICONS E ÍCONES PARA SITES
# ============================================================

# Os arquivos são organizados por finalidade.
#
# Favicon:
#   favicon-16x16.png
#   favicon-32x32.png
#   favicon.ico
#   favicon.svg
#
# Apple:
#   apple-touch-icon.png
#
# PWA:
#   icon-192x192.png
#   icon-512x512.png
#
# Compatibilidade adicional:
#   icon-48x48.png
#   icon-72x72.png
#   icon-96x96.png
#   icon-128x128.png
#   icon-144x144.png
#   icon-152x152.png
#   icon-167x167.png
#   icon-180x180.png
#   icon-256x256.png
#   icon-384x384.png
#   icon-1024x1024.png

SITE_ICON_SIZES = [
    16,
    32,
    48,
    72,
    96,
    128,
    144,
    152,
    167,
    180,
    192,
    256,
    384,
    512,
    1024,
]

# Dimensões do favicon.ico.
# O ICO conterá múltiplas resoluções em um único arquivo.
FAVICON_ICO_SIZES = [
    16,
    32,
    48,
]

# Dimensão do ícone Apple Touch.
APPLE_TOUCH_ICON_SIZE = 180

# Tamanhos dos ícones PWA.
PWA_ICON_SIZES = [
    192,
    512,
]


# Dimensões adicionais de ícones iOS (pixels).
# O arquivo AppIcon-1024.png e Contents.json formam o conjunto
# universal recomendado para projetos Xcode atuais. Os outros PNGs
# atendem a projetos/fluxos legados que ainda pedem tamanhos separados.
IOS_ICON_SIZES = [
    20, 29, 40, 58, 60, 76, 80, 87, 120, 152, 167, 180, 1024,
]

# Dimensões comuns para artes verticais de referência da App Store.
# IMPORTANTE: são artes-base com a logo centralizada, não screenshots
# reais do aplicativo. Para envio à App Store, use capturas reais do app.
APPSTORE_IMAGE_SIZES = [
    (1290, 2796),  # iPhone 6,9"
    (1260, 2736),  # iPhone 6,5" / tamanhos recentes compatíveis
    (1242, 2688),  # iPhone 6,5" legado
    (2048, 2732),  # iPad Pro 12,9"
    (2064, 2752),  # iPad Pro 13"
]

# Dimensões da imagem Open Graph para compartilhamento.
#
# Proporção recomendada: 1200x630.
SHARE_IMAGE_SIZE = (1200, 630)

# Ícones maskable para aplicações PWA.
MASKABLE_ICON_SIZES = [
    192,
    512,
]

# Padding interno dos ícones maskable.
#
# A área segura é mantida dentro de aproximadamente 80%
# da dimensão total para reduzir cortes em formatos adaptativos.
MASKABLE_SAFE_AREA = 0.80


# ============================================================
# CAMINHOS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SOURCE_PATH = os.path.join(BASE_DIR, SOURCE_IMAGE)

ANDROID_OUTPUT_PATH = os.path.join(
    BASE_DIR,
    ANDROID_OUTPUT,
)

PLAYSTORE_OUTPUT_PATH = os.path.join(
    BASE_DIR,
    PLAYSTORE_OUTPUT,
)

SITE_OUTPUT_PATH = os.path.join(
    BASE_DIR,
    SITE_OUTPUT,
)


IOS_OUTPUT_PATH = os.path.join(
    BASE_DIR,
    IOS_OUTPUT,
)

APPSTORE_OUTPUT_PATH = os.path.join(
    BASE_DIR,
    APPSTORE_OUTPUT,
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def hex_to_rgb(hex_color: str):
    """Converte uma cor hexadecimal para RGB."""
    hex_color = hex_color.strip().lstrip("#")

    if len(hex_color) != 6:
        raise ValueError(
            "A cor deve estar no formato hexadecimal #RRGGBB."
        )

    try:
        return tuple(
            int(hex_color[index:index + 2], 16)
            for index in (0, 2, 4)
        )
    except ValueError as error:
        raise ValueError(
            "A cor hexadecimal informada é inválida."
        ) from error


def rgb_to_hex(color):
    """Converte uma tupla RGB para hexadecimal."""
    return "#{:02X}{:02X}{:02X}".format(*color)


def has_transparency(image: Image.Image):
    """Verifica se a imagem possui pixels transparentes."""
    if "A" not in image.getbands():
        return False

    return image.getchannel("A").getextrema()[0] < 255


def get_border_color(image: Image.Image):
    """Obtém a cor predominante das bordas da imagem."""
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
    Determina a cor de fundo.

    Imagens transparentes:
        utilizam BACKGROUND_COLOR.

    Imagens sem transparência:
        utilizam a mediana das bordas.
    """
    if has_transparency(image):
        return hex_to_rgb(BACKGROUND_COLOR)

    return get_border_color(image)


def flatten_image(image: Image.Image, background_color):
    """Aplica a cor de fundo e converte a imagem para RGB."""
    background = Image.new(
        "RGBA",
        image.size,
        background_color + (255,),
    )

    foreground = image.convert("RGBA")

    background.alpha_composite(foreground)

    return background.convert("RGB")


def crop_center_square(image: Image.Image):
    """Recorta o maior quadrado possível a partir do centro."""
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


def resize_contain(
    image: Image.Image,
    target_size: tuple[int, int],
    padding_percent: float = 0,
):
    """
    Redimensiona a imagem preservando a proporção.

    O conteúdo é centralizado dentro da dimensão solicitada,
    respeitando o percentual de padding informado.
    """
    width, height = target_size

    if width <= 0 or height <= 0:
        raise ValueError(
            "As dimensões da imagem devem ser maiores que zero."
        )

    if not 0 <= padding_percent < 50:
        raise ValueError(
            "O padding deve estar entre 0% e 50%."
        )

    padding_x = round(width * padding_percent / 100)
    padding_y = round(height * padding_percent / 100)

    available_width = max(1, width - 2 * padding_x)
    available_height = max(1, height - 2 * padding_y)

    scale = min(
        available_width / image.width,
        available_height / image.height,
    )

    new_width = max(1, round(image.width * scale))
    new_height = max(1, round(image.height * scale))

    return image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS,
    )


def create_canvas(
    image: Image.Image,
    target_size: tuple[int, int],
    background_color,
    padding_percent: float = 0,
):
    """Cria uma tela com fundo e centraliza a imagem com padding."""
    width, height = target_size

    canvas = Image.new(
        "RGB",
        (width, height),
        background_color,
    )

    resized = resize_contain(
        image,
        target_size,
        padding_percent,
    )

    x = (width - resized.width) // 2
    y = (height - resized.height) // 2

    canvas.paste(
        resized,
        (x, y),
    )

    return canvas


def resize_logo_canvas(
    image: Image.Image,
    size: int,
    background_color=None,
):
    """Redimensiona a logo sem padding artificial, preservando a proporção."""
    source = image.convert("RGBA")
    scale = min(size / source.width, size / source.height)
    new_size = (
        max(1, round(source.width * scale)),
        max(1, round(source.height * scale)),
    )
    resized = source.resize(new_size, Image.Resampling.LANCZOS)

    if background_color is None:
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    else:
        canvas = Image.new("RGBA", (size, size), background_color + (255,))

    x = (size - resized.width) // 2
    y = (size - resized.height) // 2
    canvas.alpha_composite(resized, (x, y))
    return canvas


def save_png(image: Image.Image, output_path: str):
    """Salva uma imagem PNG otimizada."""
    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True,
    )

    image.save(
        output_path,
        format="PNG",
        optimize=True,
    )


def save_jpeg(image: Image.Image, output_path: str):
    """Salva uma imagem JPEG otimizada."""
    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True,
    )

    image.convert("RGB").save(
        output_path,
        format="JPEG",
        quality=92,
        optimize=True,
        progressive=True,
    )


# ============================================================
# GERAÇÃO DOS ÍCONES ANDROID
# ============================================================

def generate_android_icons(image: Image.Image):
    """Gera todos os tamanhos de ícones Android."""
    print()
    print("=" * 60)
    print("GERANDO ÍCONES ANDROID")
    print("=" * 60)

    square = crop_center_square(image)

    os.makedirs(
        ANDROID_OUTPUT_PATH,
        exist_ok=True,
    )

    for folder, size in ANDROID_SIZES.items():
        output_folder = os.path.join(
            ANDROID_OUTPUT_PATH,
            folder,
        )

        os.makedirs(
            output_folder,
            exist_ok=True,
        )

        resized = resize_logo_canvas(image, size)

        output_path = os.path.join(
            output_folder,
            "ic_launcher.png",
        )

        save_png(
            resized,
            output_path,
        )

        print(
            f"OK: {ANDROID_OUTPUT}/{folder}/ic_launcher.png "
            f"({size}x{size})"
        )


# ============================================================
# GERAÇÃO DAS IMAGENS DA PLAY STORE
# ============================================================

def generate_playstore_images(
    image: Image.Image,
    background_color,
):
    """Gera todas as imagens nos tamanhos da Play Store."""
    print()
    print("=" * 60)
    print("GERANDO IMAGENS DA PLAY STORE")
    print("=" * 60)

    os.makedirs(
        PLAYSTORE_OUTPUT_PATH,
        exist_ok=True,
    )

    flattened_image = flatten_image(
        image,
        background_color,
    )

    for width, height in PLAYSTORE_SIZES:
        canvas = create_canvas(
            flattened_image,
            (width, height),
            background_color,
            PLAYSTORE_PADDING,
        )

        output_path = os.path.join(
            PLAYSTORE_OUTPUT_PATH,
            f"{width}x{height}.png",
        )

        save_png(
            canvas,
            output_path,
        )

        print(
            f"OK: {PLAYSTORE_OUTPUT}/{width}x{height}.png"
        )


# ============================================================
# GERAÇÃO DOS ÍCONES IOS
# ============================================================

def generate_ios_icons(image: Image.Image, background_color):
    """
    Gera PNGs de ícones iOS e um AppIcon.appiconset importável no Xcode.

    O ícone é quadrado e não recebe cantos arredondados: o iOS aplica
    a máscara visual automaticamente. A transparência é preservada
    nos PNGs de ícone, exceto quando a origem já não possui alpha.
    """
    print()
    print("=" * 60)
    print("GERANDO ÍCONES IOS")
    print("=" * 60)

    output_folder = os.path.join(IOS_OUTPUT_PATH, "AppIcon.appiconset")
    os.makedirs(output_folder, exist_ok=True)

    # Ícones iOS devem ser opacos; aplica o fundo configurado.
    source = flatten_image(image, background_color).convert("RGBA")

    for size in IOS_ICON_SIZES:
        resized = resize_logo_canvas(source, size, background_color)
        filename = f"AppIcon-{size}.png"
        output_path = os.path.join(output_folder, filename)
        save_png(resized, output_path)

        print(f"OK: {IOS_OUTPUT}/AppIcon.appiconset/{filename} ({size}x{size})")

    # Formato universal de App Icon utilizado pelas versões atuais do Xcode.
    contents = {
        "images": [
            {
                "filename": "AppIcon-1024.png",
                "idiom": "universal",
                "platform": "ios",
                "size": "1024x1024",
            }
        ],
        "info": {
            "author": "xcode",
            "version": 1,
        },
    }

    contents_path = os.path.join(output_folder, "Contents.json")
    with open(contents_path, "w", encoding="utf-8") as file:
        json.dump(contents, file, ensure_ascii=False, indent=4)

    print(f"OK: {IOS_OUTPUT}/AppIcon.appiconset/Contents.json")


# ============================================================
# GERAÇÃO DAS ARTES-BASE PARA A APP STORE
# ============================================================

def generate_appstore_images(image: Image.Image, background_color):
    """
    Gera artes-base nas proporções comuns usadas na App Store.

    Estas imagens têm a logo centralizada em um fundo sólido. Não são
    screenshots reais de um aplicativo e devem ser substituídas por
    capturas do app antes do envio para revisão da App Store.
    """
    print()
    print("=" * 60)
    print("GERANDO ARTES-BASE PARA A APP STORE")
    print("=" * 60)

    os.makedirs(APPSTORE_OUTPUT_PATH, exist_ok=True)

    flattened_image = flatten_image(image, background_color)

    for width, height in APPSTORE_IMAGE_SIZES:
        canvas = create_canvas(
            flattened_image,
            (width, height),
            background_color,
            padding_percent=20,
        )
        filename = f"{width}x{height}.png"
        output_path = os.path.join(APPSTORE_OUTPUT_PATH, filename)
        save_png(canvas, output_path)

        print(f"OK: {APPSTORE_OUTPUT}/{filename}")

    readme_path = os.path.join(APPSTORE_OUTPUT_PATH, "LEIA-ME.txt")
    with open(readme_path, "w", encoding="utf-8") as file:
        file.write(
            "Estas imagens são artes-base geradas a partir da logo, "
            "com fundo sólido e logo centralizada.\\n"
            "Elas NÃO são screenshots reais do aplicativo.\\n"
            "Para enviar o app à App Store, capture telas reais do "
            "aplicativo nos tamanhos aceitos atualmente pelo App Store Connect.\\n"
        )
    print(f"OK: {APPSTORE_OUTPUT}/LEIA-ME.txt")


# ============================================================
# GERAÇÃO DO FAVICON ICO
# ============================================================

def generate_favicon_ico(image: Image.Image):
    """
    Gera favicon.ico com múltiplas resoluções.

    O formato ICO contém imagens incorporadas de 16, 32 e 48 px,
    evitando a necessidade de arquivos ICO separados.
    """
    output_path = os.path.join(
        SITE_OUTPUT_PATH,
        "favicon.ico",
    )

    square = crop_center_square(image).convert("RGBA")

    # O Pillow gera um ICO com os tamanhos solicitados.
    square.save(
        output_path,
        format="ICO",
        sizes=[
            (size, size)
            for size in FAVICON_ICO_SIZES
        ],
    )

    print(
        f"OK: {SITE_OUTPUT}/favicon.ico "
        f"({', '.join(str(s) for s in FAVICON_ICO_SIZES)} px)"
    )


# ============================================================
# GERAÇÃO DOS FAVICONS PNG E ÍCONES APPLE
# ============================================================

def generate_site_png_icons(image: Image.Image):
    """Gera os ícones PNG utilizados por sites e dispositivos."""
    print()
    print("=" * 60)
    print("GERANDO FAVICONS E ÍCONES PARA SITES")
    print("=" * 60)

    os.makedirs(
        SITE_OUTPUT_PATH,
        exist_ok=True,
    )

    for size in SITE_ICON_SIZES:
        resized = resize_logo_canvas(image, size)

        output_path = os.path.join(
            SITE_OUTPUT_PATH,
            f"icon-{size}x{size}.png",
        )

        save_png(
            resized,
            output_path,
        )

        print(
            f"OK: {SITE_OUTPUT}/icon-{size}x{size}.png"
        )

    # Favicons com nomes convencionais.
    for size in (16, 32):
        source_path = os.path.join(
            SITE_OUTPUT_PATH,
            f"icon-{size}x{size}.png",
        )

        output_path = os.path.join(
            SITE_OUTPUT_PATH,
            f"favicon-{size}x{size}.png",
        )

        with Image.open(source_path) as generated:
            save_png(
                generated.copy(),
                output_path,
            )

        print(
            f"OK: {SITE_OUTPUT}/favicon-{size}x{size}.png"
        )

    # Ícone utilizado ao adicionar o site à tela inicial Apple.
    apple_icon = resize_logo_canvas(image, APPLE_TOUCH_ICON_SIZE)

    save_png(
        apple_icon,
        os.path.join(
            SITE_OUTPUT_PATH,
            "apple-touch-icon.png",
        ),
    )

    print(
        f"OK: {SITE_OUTPUT}/apple-touch-icon.png "
        f"({APPLE_TOUCH_ICON_SIZE}x{APPLE_TOUCH_ICON_SIZE})"
    )


# ============================================================
# GERAÇÃO DOS ÍCONES MASKABLE
# ============================================================

def generate_maskable_icons(
    image: Image.Image,
    background_color,
):
    """
    Gera ícones PWA maskable redimensionando a logo sem padding artificial.
    Observação: sem área segura, máscaras do sistema podem cortar partes da logo.
    """
    print()
    print("=" * 60)
    print("GERANDO ÍCONES MASKABLE")
    print("=" * 60)

    for size in MASKABLE_ICON_SIZES:
        canvas = resize_logo_canvas(image, size, background_color).convert("RGB")

        output_path = os.path.join(
            SITE_OUTPUT_PATH,
            f"icon-{size}x{size}-maskable.png",
        )

        save_png(
            canvas,
            output_path,
        )

        print(
            f"OK: {SITE_OUTPUT}/icon-{size}x{size}-maskable.png"
        )


# ============================================================
# GERAÇÃO DA IMAGEM DE COMPARTILHAMENTO
# ============================================================

def generate_share_image(
    image: Image.Image,
    background_color,
):
    """
    Gera a miniatura horizontal utilizada no compartilhamento.

    Dimensão:
        1200x630 px.

    O padding segue a mesma lógica utilizada nas artes da
    Play Store, com uma configuração independente.

    O resultado fica em site-images/share.png.
    """
    print()
    print("=" * 60)
    print("GERANDO IMAGEM DE COMPARTILHAMENTO")
    print("=" * 60)

    if SHARE_BACKGROUND_COLOR is not None:
        share_background = hex_to_rgb(
            SHARE_BACKGROUND_COLOR
        )
    else:
        share_background = background_color

    flattened_image = flatten_image(
        image,
        share_background,
    )

    share_canvas = create_canvas(
        flattened_image,
        SHARE_IMAGE_SIZE,
        share_background,
        SHARE_PADDING,
    )

    output_path = os.path.join(
        SITE_OUTPUT_PATH,
        "share.png",
    )

    save_png(
        share_canvas,
        output_path,
    )

    print(
        f"OK: {SITE_OUTPUT}/share.png "
        f"({SHARE_IMAGE_SIZE[0]}x{SHARE_IMAGE_SIZE[1]})"
    )


# ============================================================
# GERAÇÃO DO FAVICON SVG
# ============================================================

def generate_favicon_svg():
    """
    Gera favicon.svg utilizando a logo como referência.

    Como o Pillow não exporta SVG vetorial a partir de uma
    imagem rasterizada, este arquivo contém a imagem PNG
    incorporada em base64 somente se necessário.

    Para manter o arquivo simples e independente, o SVG
    utiliza a versão PNG de 32x32 embutida em formato base64.
    """
    import base64

    png_path = os.path.join(
        SITE_OUTPUT_PATH,
        "favicon-32x32.png",
    )

    with open(png_path, "rb") as file:
        encoded_image = base64.b64encode(
            file.read()
        ).decode("ascii")

    svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="32"
     height="32"
     viewBox="0 0 32 32">
    <image
        href="data:image/png;base64,{encoded_image}"
        width="32"
        height="32"
        preserveAspectRatio="xMidYMid meet"
    />
</svg>
"""

    output_path = os.path.join(
        SITE_OUTPUT_PATH,
        "favicon.svg",
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(svg_content)

    print(
        f"OK: {SITE_OUTPUT}/favicon.svg"
    )


# ============================================================
# GERAÇÃO DO SVG PARA ABAS FIXADAS DO SAFARI
# ============================================================

def generate_safari_pinned_tab():
    """
    Gera um SVG monocromático simplificado para o Safari.

    O recurso é opcional. Como a logo de origem pode conter
    múltiplas cores, o arquivo usa a silhueta alfa da imagem
    convertida em um caminho SVG.
    """
    image_path = os.path.join(
        SITE_OUTPUT_PATH,
        "icon-32x32.png",
    )

    with Image.open(image_path) as source:
        image = source.convert("RGBA")

    alpha = image.getchannel("A")

    # Converte os pixels visíveis em um conjunto de retângulos.
    # O resultado permanece vetorial, embora possa ter muitos
    # elementos quando a imagem possui detalhes pequenos.
    pixels = np.asarray(alpha)

    rects = []

    for y in range(pixels.shape[0]):
        for x in range(pixels.shape[1]):
            if pixels[y, x] > 127:
                rects.append(
                    f'<rect x="{x}" y="{y}" width="1" height="1"/>'
                )

    svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 32 32">
    <g fill="{SAFARI_PINNED_COLOR}">
        {''.join(rects)}
    </g>
</svg>
"""

    output_path = os.path.join(
        SITE_OUTPUT_PATH,
        "safari-pinned-tab.svg",
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(svg_content)

    print(
        f"OK: {SITE_OUTPUT}/safari-pinned-tab.svg"
    )


# ============================================================
# GERAÇÃO DO MANIFESTO PWA
# ============================================================

def generate_web_manifest():
    """Gera o manifesto de instalação da aplicação web."""
    manifest = {
        "id": PWA_START_URL,
        "name": SITE_NAME,
        "short_name": SITE_SHORT_NAME,
        "description": SITE_DESCRIPTION,
        "lang": "pt-BR",
        "start_url": PWA_START_URL,
        "scope": "/",
        "display": "standalone",
        "orientation": "any",
        "theme_color": THEME_COLOR,
        "background_color": THEME_COLOR,
        "icons": [],
    }

    for size in PWA_ICON_SIZES:
        manifest["icons"].append({
            "src": f"/icon-{size}x{size}.png",
            "sizes": f"{size}x{size}",
            "type": "image/png",
            "purpose": "any",
        })

    for size in MASKABLE_ICON_SIZES:
        manifest["icons"].append({
            "src": f"/icon-{size}x{size}-maskable.png",
            "sizes": f"{size}x{size}",
            "type": "image/png",
            "purpose": "maskable",
        })

    output_path = os.path.join(
        SITE_OUTPUT_PATH,
        "site.webmanifest",
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            manifest,
            file,
            ensure_ascii=False,
            indent=4,
        )

    print(
        f"OK: {SITE_OUTPUT}/site.webmanifest"
    )


# ============================================================
# GERAÇÃO DA CONFIGURAÇÃO LEGADA DO WINDOWS
# ============================================================

def generate_windows_config():
    """Gera browserconfig.xml para ambientes Windows legados."""
    if not GENERATE_WINDOWS_CONFIG:
        return

    xml_content = f"""<?xml version="1.0" encoding="utf-8"?>
<browserconfig>
    <msapplication>
        <tile>
            <square150x150logo src="/icon-152x152.png"/>
            <TileColor>{THEME_COLOR}</TileColor>
        </tile>
    </msapplication>
</browserconfig>
"""

    output_path = os.path.join(
        SITE_OUTPUT_PATH,
        "browserconfig.xml",
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(xml_content)

    print(
        f"OK: {SITE_OUTPUT}/browserconfig.xml"
    )


# ============================================================
# GERAÇÃO DOS METADADOS HTML
# ============================================================

def generate_html_head():
    """
    Gera um arquivo com as principais tags que podem ser
    copiadas para o <head> do site.
    """
    html_content = """<!-- Favicons -->
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-16x16.png" type="image/png" sizes="16x16">
<link rel="icon" href="/favicon-32x32.png" type="image/png" sizes="32x32">

<!-- Apple -->
<link rel="apple-touch-icon" href="/apple-touch-icon.png">

<!-- PWA -->
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="THEME_COLOR">

<!-- Safari -->
<link rel="mask-icon" href="/safari-pinned-tab.svg" color="SAFARI_PINNED_COLOR">

<!-- Windows legado -->
<meta name="msapplication-config" content="/browserconfig.xml">
<meta name="msapplication-TileColor" content="THEME_COLOR">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:title" content="SITE_NAME">
<meta property="og:description" content="SITE_DESCRIPTION">
<meta property="og:image" content="https://example.com/share.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="SITE_NAME">
<meta property="og:locale" content="pt_BR">

<!-- X / Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="SITE_NAME">
<meta name="twitter:description" content="SITE_DESCRIPTION">
<meta name="twitter:image" content="https://example.com/share.png">
"""

    html_content = (
        html_content
        .replace("THEME_COLOR", THEME_COLOR)
        .replace("SAFARI_PINNED_COLOR", SAFARI_PINNED_COLOR)
        .replace("SITE_NAME", SITE_NAME)
        .replace("SITE_DESCRIPTION", SITE_DESCRIPTION)
    )

    output_path = os.path.join(
        SITE_OUTPUT_PATH,
        "html-head.html",
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(html_content)

    print(
        f"OK: {SITE_OUTPUT}/html-head.html"
    )


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def main():
    """Executa todas as rotinas de geração."""
    print("=" * 60)
    print("GERADOR DE ÍCONES E IMAGENS")
    print("=" * 60)

    print(f"Imagem de origem: {SOURCE_IMAGE}")
    print(f"Fundo configurado: {BACKGROUND_COLOR}")
    print(f"Padding Play Store: {PLAYSTORE_PADDING}%")
    print(f"Padding compartilhamento: {SHARE_PADDING}%")

    # Verifica se a imagem de origem existe.
    if not os.path.isfile(SOURCE_PATH):
        print()
        print("ERRO: imagem não encontrada:")
        print(SOURCE_PATH)
        print()
        return

    # Valida as configurações de cores.
    try:
        hex_to_rgb(BACKGROUND_COLOR)
        hex_to_rgb(THEME_COLOR)
        hex_to_rgb(SAFARI_PINNED_COLOR)

        if SHARE_BACKGROUND_COLOR is not None:
            hex_to_rgb(SHARE_BACKGROUND_COLOR)

    except ValueError as error:
        print()
        print(f"ERRO: {error}")
        print()
        return

    # Carrega a imagem de origem.
    try:
        with Image.open(SOURCE_PATH) as source:
            image = source.convert("RGBA")

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

    # Calcula a cor de fundo a ser utilizada.
    background_color = get_background_color(image)

    print(
        f"Fundo detectado: {rgb_to_hex(background_color)}"
    )

    # Gera os ícones Android.
    generate_android_icons(image)

    # Gera os ícones iOS e o AppIcon.appiconset para Xcode.
    generate_ios_icons(image, background_color)

    # Gera artes-base nos tamanhos comuns da App Store.
    generate_appstore_images(image, background_color)

    # Gera as imagens da Play Store.
    generate_playstore_images(
        image,
        background_color,
    )

    # Gera os favicons e ícones de sites.
    generate_site_png_icons(image)

    # Gera o favicon ICO.
    generate_favicon_ico(image)

    # Gera as versões maskable para PWA.
    generate_maskable_icons(
        image,
        hex_to_rgb(BACKGROUND_COLOR),
    )

    # Gera a miniatura de compartilhamento.
    generate_share_image(
        image,
        background_color,
    )

    # Gera os arquivos de configuração do site.
    generate_favicon_svg()
    generate_safari_pinned_tab()
    generate_web_manifest()
    generate_windows_config()
    generate_html_head()

    print()
    print("=" * 60)
    print("GERAÇÃO CONCLUÍDA")
    print("=" * 60)
    print()
    print(f"Ícones Android: {ANDROID_OUTPUT_PATH}")
    print(f"Ícones iOS: {IOS_OUTPUT_PATH}")
    print(f"Artes-base App Store: {APPSTORE_OUTPUT_PATH}")
    print(f"Imagens Play Store: {PLAYSTORE_OUTPUT_PATH}")
    print(f"Ícones e imagens do site: {SITE_OUTPUT_PATH}")
    print()


if __name__ == "__main__":
    main()