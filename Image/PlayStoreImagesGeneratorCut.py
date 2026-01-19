from PIL import Image
import os

# ============================================================
# CONFIGURATION
# ============================================================

# Image source
SOURCE_IMAGE = "Image/image.png"

# Output sizes (Google Play Store)
SIZES = [

    # ------------------------------------------------------------
    # App Icon (Play Store)
    # ------------------------------------------------------------
    (512, 512),

    # ------------------------------------------------------------
    # Feature Graphic (OBRIGATÓRIO)
    # ------------------------------------------------------------
    (1024, 500),

    # ------------------------------------------------------------
    # Phone Screenshots (portrait - recomendado)
    # ------------------------------------------------------------
    (1080, 1920),
    (1242, 2208),
    (1440, 2560),

    # ------------------------------------------------------------
    # Phone Screenshots (landscape)
    # ------------------------------------------------------------
    (1920, 1080),
    (2560, 1440),

    # ------------------------------------------------------------
    # Tablet Screenshots
    # ------------------------------------------------------------
    (1200, 1920),   # 7"
    (1600, 2560),   # 10"

    # ------------------------------------------------------------
    # Wear OS (square)
    # ------------------------------------------------------------
    (384, 384),

    # ------------------------------------------------------------
    # Android TV
    # ------------------------------------------------------------
    (1280, 720),    # TV Banner
    (1920, 1080),   # TV Screenshot
]


# Output format
OUTPUT_FORMAT = "PNG"

# ============================================================
# FUNCTIONS
# ============================================================

def crop_cover(img, target_width, target_height):
    """
    Resize and crop image to fill target size (cover behavior)
    """
    src_width, src_height = img.size
    src_ratio = src_width / src_height
    target_ratio = target_width / target_height

    # Resize
    if src_ratio > target_ratio:
        # Image is wider
        new_height = target_height
        new_width = int(new_height * src_ratio)
    else:
        # Image is taller
        new_width = target_width
        new_height = int(new_width / src_ratio)

    img = img.resize((new_width, new_height), Image.LANCZOS)

    # Center crop
    left = (new_width - target_width) // 2
    top = (new_height - target_height) // 2
    right = left + target_width
    bottom = top + target_height

    return img.crop((left, top, right, bottom))


# ============================================================
# MAIN
# ============================================================

def main():
    img = Image.open(SOURCE_IMAGE).convert("RGBA")

    base_name = os.path.splitext(os.path.basename(SOURCE_IMAGE))[0]

    for width, height in SIZES:
        result = crop_cover(img, width, height)

        output_name = f"{base_name}-{width}x{height}.png"
        result.save(output_name, OUTPUT_FORMAT)

        print(f"Exported: {output_name}")

    print("Done!")


if __name__ == "__main__":
    main()
