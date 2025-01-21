#1080 x 1920
#720 x 1280
#480 x 854
#360 x 640
#240 x 426
#120 x 213

import os
from moviepy.editor import VideoFileClip

def crop_and_center(input_file, output_file):
    # Load the original video
    video = VideoFileClip(input_file)

    # Define the dimensions for Reels
    reels_width = 1080
    reels_height = 1920

    # Calculate the aspect ratios for Reels and the video
    reels_aspect_ratio = reels_width / reels_height
    video_aspect_ratio = video.size[0] / video.size[1]

    if video_aspect_ratio > reels_aspect_ratio:
        # The video is wider than Reels, so adjust the width
        new_width = reels_aspect_ratio * video.size[1]
        video = video.crop(x1=(video.size[0] - new_width) // 2, x2=(video.size[0] + new_width) // 2)
    else:
        # The video is taller than Reels, so adjust the height
        new_height = video.size[0] / reels_aspect_ratio
        video = video.crop(y1=(video.size[1] - new_height) // 2, y2=(video.size[1] + new_height) // 2)

    # Resize the video to the Reels dimensions
    video = video.resize((reels_width, reels_height))

    # Save the cropped and centered video in Reels format with the same duration as the original
    video.write_videofile(output_file, codec='libx264', audio_codec="aac")

# Get the list of files in the root folder
root_folder = "./videos/"  # Path to the root folder
output_folder = "./cropped_videos/"
if not os.path.exists(output_folder):
    # Create the folder
    os.makedirs(output_folder)

files = os.listdir(root_folder)

# Filter video files
videos = [file for file in files if file.endswith((".mpeg", ".mp4", ".avi", ".mov"))]

# Crop and save each video with the suffix "_reels"
for video in videos:
    input_file = os.path.join(root_folder, video)
    output_file = os.path.join(output_folder, video.split(".")[0] + "_cropped.mp4")
    crop_and_center(input_file, output_file)
