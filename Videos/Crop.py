from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip

# ============================================================
# CONFIGURATION
# ============================================================

SOURCE_VIDEO = "Videos/input.mp4"
OUTPUT_VIDEO = "Videos/output.mp4"

# Canvas size (mobile fullscreen default)
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1920

# Background color (RGB)
BACKGROUND_COLOR = (11, 11, 11)

# Crop control
# 1.0  = no crop (contain)
# 1.05 = 5% crop
# 1.10 = 10% crop
CROP_FACTOR = 1.90

# Output
FPS = 30
CODEC = "libx264"
AUDIO_CODEC = "aac"

# ============================================================
# PROCESS
# ============================================================

def main():
    video = VideoFileClip(SOURCE_VIDEO)

    vw, vh = video.size
    canvas_ratio = CANVAS_WIDTH / CANVAS_HEIGHT
    video_ratio = vw / vh

    # Base scale (contain)
    if video_ratio > canvas_ratio:
        scale = CANVAS_WIDTH / vw
    else:
        scale = CANVAS_HEIGHT / vh

    # Apply extra zoom (controlled crop)
    scale *= CROP_FACTOR

    video_resized = video.resize(scale)

    # Background canvas
    background = ColorClip(
        size=(CANVAS_WIDTH, CANVAS_HEIGHT),
        color=BACKGROUND_COLOR,
        duration=video.duration
    )

    # Center video
    final = CompositeVideoClip(
        [
            background,
            video_resized.set_position("center")
        ],
        size=(CANVAS_WIDTH, CANVAS_HEIGHT)
    )

    final.write_videofile(
        OUTPUT_VIDEO,
        fps=FPS,
        codec=CODEC,
        audio_codec=AUDIO_CODEC,
        threads=4
    )

    print("Done!")
    print(f"Exported: {OUTPUT_VIDEO}")

if __name__ == "__main__":
    main()
