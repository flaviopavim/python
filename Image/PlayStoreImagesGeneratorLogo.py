from PIL import Image
import os
import numpy as np

# ============================================================
# CONFIGURATION
# ============================================================

SOURCE_IMAGE = "Image/logo.png"

# Background color:
# - HEX string: "#121212"
# - RGB tuple: (18, 18, 18)
# - None -> auto dominant color
BACKGROUND_COLOR = "#0b0b0b"

# Padding configuration
PADDING = None              # pixels (None to disable)
PADDING_PERCENT = 0.20    # e.g. 0.08 for 8% (used only if PADDING is None)

SIZES = [
    (512, 512),
    (1024, 500),
    (1080, 1920),
    (1242, 2208),
    (1440, 2560),
    (1920, 1080),
    (2560, 1440),
    (1200, 1920),
    (1600, 2560),
    (384, 384),
    (1280, 720),
]

OUTPUT_FORMAT = "PNG"

# ============================================================
# FUNCTIONS
# ============================================================

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def get_dominant_color(img, border_size=10):
    np_img = np.array(img)

    if np_img.shape[2] == 4:
        np_img = np_img[:, :, :3]

    h, w, _ = np_img.shape

    top = np_img[0:border_size, :, :]
    bottom = np_img[h-border_size:h, :, :]
    left = np_img[:, 0:border_size, :]
    right = np_img[:, w-border_size:w, :]

    avg_color = (
        top.mean(axis=(0, 1)) +
        bottom.mean(axis=(0, 1)) +
        left.mean(axis=(0, 1)) +
        right.mean(axis=(0, 1))
    ) / 4

    return tuple(avg_color.astype(int))


def resolve_background_color(img):
    if BACKGROUND_COLOR is None:
        return get_dominant_color(img)

    if isinstance(BACKGROUND_COLOR, tuple):
        return BACKGROUND_COLOR

    if isinstance(BACKGROUND_COLOR, str):
        return hex_to_rgb(BACKGROUND_COLOR)

    raise ValueError("Invalid BACKGROUND_COLOR format")


def resolve_padding(target_width, target_height):
    """
    Resolve padding in pixels
    """
    if PADDING is not None:
        return PADDING

    if PADDING_PERCENT is not None:
        return int(min(target_width, target_height) * PADDING_PERCENT)

    return 0


def resize_contain(img, target_width, target_height):
    """
    Resize image to fit entirely inside target canvas,
    applying padding and background color
    """
    padding = resolve_padding(target_width, target_height)

    usable_width = target_width - padding * 2
    usable_height = target_height - padding * 2

    if usable_width <= 0 or usable_height <= 0:
        raise ValueError("Padding too large for target size")

    src_width, src_height = img.size
    src_ratio = src_width / src_height
    target_ratio = usable_width / usable_height

    # Resize (contain)
    if src_ratio > target_ratio:
        new_width = usable_width
        new_height = int(new_width / src_ratio)
    else:
        new_height = usable_height
        new_width = int(new_height * src_ratio)

    img_resized = img.resize((new_width, new_height), Image.LANCZOS)

    bg_color = resolve_background_color(img)

    canvas = Image.new("RGB", (target_width, target_height), bg_color)

    x = (target_width - new_width) // 2
    y = (target_height - new_height) // 2

    canvas.paste(
        img_resized,
        (x, y),
        img_resized if img_resized.mode == "RGBA" else None
    )

    return canvas


# ============================================================
# MAIN
# ============================================================

def main():
    img = Image.open(SOURCE_IMAGE).convert("RGBA")

    base_name = os.path.splitext(os.path.basename(SOURCE_IMAGE))[0]

    for width, height in SIZES:
        result = resize_contain(img, width, height)

        output_name = f"{base_name}-{width}x{height}.png"
        result.save(output_name, OUTPUT_FORMAT)

        print(f"Exported: {output_name}")

    print("Done!")


if __name__ == "__main__":
    main()
