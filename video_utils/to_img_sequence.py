import os,sys
import subprocess

def to_img_sequence(in_path,out_path,fps):
    for folder in os.listdir(in_path):
        os.makedirs(os.path.join(out_path,folder),exist_ok=True)
        for video in os.listdir(os.path.join(in_path,folder)):
            os.makedirs(os.path.join(out_path,folder,video),exist_ok=True)
            subprocess.run(["ffmpeg", "-i", os.path.join(in_path,folder,video), "-vf", f"fps={fps}", os.path.join(out_path,folder,video,"img%d.png")])