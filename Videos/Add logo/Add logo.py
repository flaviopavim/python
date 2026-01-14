#import pycuda.autoinit
import os
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def add_logo_to_videos_in_folder(root_folder, logo_path):
    # Get the list of files in the root folder
    files = os.listdir(root_folder)

    # Filter video files
    videos = [file for file in files if file.endswith((".mpeg", ".mp4", ".avi", ".mov"))]

    # For each video, add the logo and save it with the same name but with the suffix "_logo"
    for video in videos:
        file_name = os.path.join(root_folder, video)
        output_name = os.path.join(root_folder, video.split(".")[0] + "_logo.mp4")
        add_logo_to_video(file_name, logo_path, output_name)

def add_logo_to_video(video_path, logo_path, output_path):
    # Load the original video
    video = VideoFileClip(video_path)

    # Load the PNG logo image with transparency
    logo = ImageClip(logo_path).set_duration(video.duration)

    # Set the logo position 10 pixels from the top and 10 pixels from the right
    logo = logo.set_position(lambda t: (video.size[0] - logo.size[0] - 10, 10))
    # Set the logo position 10 pixels from the bottom and 10 pixels from the right
    #logo = logo.set_position(lambda t: (video.size[0] - logo.size[0] - 10, video.size[1] - logo.size[1] - 10))

    # Compose the original video with the logo
    video_with_logo = CompositeVideoClip([video, logo])

    # Save the resulting video
    video_with_logo.write_videofile(output_path, codec='libx264', audio_codec="aac")

# Example usage
root_folder = "./"
logo_path = "./logo.png"

add_logo_to_videos_in_folder(root_folder, logo_path)
