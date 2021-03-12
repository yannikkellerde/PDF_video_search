from PIL import Image
import pytesseract
import os
from tqdm import tqdm
import pickle

output_dict = {}

for folder in tqdm(os.listdir("images"),leave=False,desc="Outer"):
    for video in tqdm(os.listdir(os.path.join("images",folder)),leave=False,desc="Videos"):
        for image in tqdm(os.listdir(os.path.join("images",folder,video)),leave=False,desc="Images"):
            orig = pytesseract.image_to_string(Image.open(os.path.join("images",folder,video,image)),config='--psm 7')
            res = "".join(list(filter(lambda x:x in "0123456789",orig)))
            try:
                number = int(res)+1
            except ValueError:
                continue
            folie = int(folder.split("-")[1])
            second = int(image[3:].split(".")[0])
            key = (folie,number)
            if key in output_dict:
                if output_dict[key][0] != video:
                    try:
                        vidnum = int(video.split("_")[1].split(".")[0])
                        oldnum = int(output_dict[key][0].split("_")[1].split(".")[0])
                        if vidnum < oldnum:
                            output_dict[key] = [video,[second,second]]
                    except Exception as e:
                        print(e)
                        continue
                else:
                    output_dict[key][1][0] = min(output_dict[key][1][0],second)
                    output_dict[key][1][1] = max(output_dict[key][1][1],second)
            else:
                output_dict[key] = [video,[second,second]]

with open("slide_second_map.pkl","wb") as f:
    pickle.dump(output_dict,f)