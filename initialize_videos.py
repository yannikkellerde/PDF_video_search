import os,sys
import argparse
from shutil import rmtree

from video_utils.crop_videos import crop_videos
from video_utils.get_timestamps import create_video_map
from video_utils.to_img_sequence import to_img_sequence

parser = argparse.ArgumentParser(description='Define VP code and config files')
parser.add_argument('--input','-i',type=str,help='Input Folder containing folders of videos')
parser.add_argument('--output','-o',type=str,help='output folder')
parser.add_argument('--seconds_per_image','-s',type=float,default=1.0,help='Higher => less precise timestamps but quicker')
parser.add_argument('--top','-t',type=int,help='Y coordinate of page number location (pixels)')
parser.add_argument('--left','-l',type=int,help='X coordinate of page number location (pixels)')
parser.add_argument('--width','-w',type=int,help='Width of page number section (pixels)')
parser.add_argument('--height',"-p",type=int,help='Height of page number section (pixels)')
parser.add_argument("--clean",action="store_true",help="Delete all temporary folders after finishing")
args = parser.parse_args()

os.makedirs(args.output,exist_ok=True)
crop_videos(args.input,os.path.join(args.output,"cropped_videos"),args.left,args.top,args.width,args.height)
to_img_sequence(os.path.join(args.output,"cropped_videos"),os.path.join(args.output,"images"),fps=1/args.seconds_per_image)
create_video_map(os.path.join(args.output,"images"),os.path.join(args.output,"video_map.pkl"),seconds_per_image=args.seconds_per_image)

if args.clean:
    rmtree(os.path.join(args.output,"cropped_videos"))
    rmtree(os.path.join(args.output,"images"))