from moviepy.editor import VideoFileClip

video_clip = VideoFileClip("video.mp4")
audio_clip = video_clip.audio
audio_clip.write_audiofile("audio.mp3", codec='mp3')
video_clip.close()
audio_clip.close()
