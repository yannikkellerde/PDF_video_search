from tika import parser
import os
import pickle
import re
from tqdm import tqdm

res_dict = {}

for pdf in tqdm(os.listdir("folien")):
    raw = parser.from_file(os.path.join("folien",pdf))
    numbers = [int(x.split(" ")[-1]) for x in re.findall(r"\| {1,2}\d+",raw["content"])]
    missing_slides = 0
    for num in range(1,max(numbers)):
        if num in numbers:
            res_dict[(pdf,num-missing_slides)] = num
        else:
            missing_slides+=1

with open("slide_map.pkl","wb") as f:
    pickle.dump(res_dict,f)