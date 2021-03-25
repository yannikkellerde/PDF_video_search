import sys,os
import subprocess

def crop_videos(in_path, out_path,x,y,w,h):
    for folder in os.listdir(in_path):
        os.makedirs(os.path.join(out_path,folder),exist_ok=True)
        for video in os.listdir(os.path.join(in_path,folder)):
            subprocess.run(["ffmpeg", "-i", os.path.join(in_path,folder,video), "-filter:v", f"crop={w}:{h}:{x}:{y}", os.path.join(out_path,folder,video)])

if __name__ == "__main__":
    crop_videos(sys.argv[1],sys.argv[2])