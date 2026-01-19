from PIL import Image
import os
import numpy as np

# ============================================================
# CONFIGURATION
# ============================================================

SOURCE_IMAGE = "Image/image.png"

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

def get_dominant_color(img, border_size=10):
    """
    Get dominant color from image borders (safe version)
    """
    np_img = np.array(img)

    # Remove alpha if exists
    if np_img.shape[2] == 4:
        np_img = np_img[:, :, :3]

    h, w, _ = np_img.shape

    # Borders
    top = np_img[0:border_size, :, :]
    bottom = np_img[h-border_size:h, :, :]
    left = np_img[:, 0:border_size, :]
    right = np_img[:, w-border_size:w, :]

    # Mean color of each border
    top_mean = top.mean(axis=(0, 1))
    bottom_mean = bottom.mean(axis=(0, 1))
    left_mean = left.mean(axis=(0, 1))
    right_mean = right.mean(axis=(0, 1))

    # Global mean
    avg_color = (top_mean + bottom_mean + left_mean + right_mean) / 4

    return tuple(avg_color.astype(int))



def resize_contain(img, target_width, target_height):
    """
    Resize image to fit entirely inside target canvas,
    filling background with dominant border color
    """
    src_width, src_height = img.size
    src_ratio = src_width / src_height
    target_ratio = target_width / target_height

    # Resize (contain)
    if src_ratio > target_ratio:
        new_width = target_width
        new_height = int(new_width / src_ratio)
    else:
        new_height = target_height
        new_width = int(new_height * src_ratio)

    img_resized = img.resize((new_width, new_height), Image.LANCZOS)

    # Background color
    bg_color = get_dominant_color(img)

    # Create canvas
    canvas = Image.new("RGB", (target_width, target_height), bg_color)

    # Center image
    x = (target_width - new_width) // 2
    y = (target_height - new_height) // 2

    canvas.paste(img_resized, (x, y), img_resized if img_resized.mode == "RGBA" else None)

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
