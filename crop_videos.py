import os
import subprocess

for folder in os.listdir("videos"):
    os.makedirs(os.path.join("cropped_videos",folder),exist_ok=True)
    for video in os.listdir(os.path.join("videos",folder)):
        subprocess.run(["ffmpeg", "-i", os.path.join("videos",folder,video), "-filter:v", "crop=200:20:1000:695", os.path.join("cropped_videos",folder,video)])