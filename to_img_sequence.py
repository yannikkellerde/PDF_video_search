import os
import subprocess

for folder in os.listdir("cropped_videos"):
    os.makedirs(os.path.join("images",folder),exist_ok=True)
    for video in os.listdir(os.path.join("cropped_videos",folder)):
        os.makedirs(os.path.join("images",folder,video),exist_ok=True)
        subprocess.run(["ffmpeg", "-i", os.path.join("cropped_videos",folder,video), "-vf", "fps=1", os.path.join("images",folder,video,"img%d.png")])