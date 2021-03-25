# Search multiple PDFs and Videos using this python script.
This script can be used to quickly look up information from lectures during an open-book exam.
## Searching through multiple PDFs
**Requirements** 
+ OS: Linux, preferrably Ubuntu or another Debian based distro.
+ Python3
+ [urwid](https://pypi.org/project/urwid/)
+ [pdfgrep](https://wiki.ubuntuusers.de/pdfgrep/)
+ [evince](https://wiki.ubuntuusers.de/Evince/)

**Usage**
1. Store the PDFs you want to search into a folder
2. Run `python main.py --pdf_folder path/to/you/pdfs` from the repositories root
3. Enter your search string and hit Enter.
4. Use the arrow keys to navigate the results. Hit Enter to view the pdf at the location of the found text.
5. To enter a new search string, hit `q`.

## Searching videos that show PDFs
To search videos that show PDF Slides (For example videos of University lectures), the following conditions have to be met:
+ You have downloaded the videos as well as the PDFs
+ The PDFs are numbered and the page number is displayed at roughly the same position during all videos (or at least the parts of the videos you care about)
+ Each video only shows the slides of one PDF files (Multiple videos for one PDF file is ok, but not the other way around).

Store the pdfs into a folder. Then create a folder for your videos. In the videos folder, create a folder for every of your PDF files that is named like the pdf file (without the `.pdf`). Put your videos in the folder with the name of the PDF file that is shown in the video.  
![Video Folder](/usage_images/video_folder.png)

**Requirements**
+ The Requirements described above in the *Searching through multiple PDFs* section.
+ [tqdm](https://pypi.org/project/tqdm/)
+ [pytesseract](https://pypi.org/project/pytesseract/)
+ [vlc media player](https://wiki.ubuntuusers.de/VLC/)

**Usage**
1. Obtain the location of the page number in the videos as x,y of the top left corner and width and height of the video patch that contains the page number
2. Run `python initialize_videos.py -i your/video/folder -o output_folder_name -s 1 --top Y --left X --width W --height H`. Replace Y,X,W,H with the coordinates you measured in the last step. You can tune the number after -s to speed up the process. Larger -s means quicker initialization of the timestamps while smaller -s means more exact timestamps.
3. In the output folder you specified you should now find a file called `video_map.pkl`. This file contains the matches from your PDF page numbers to video timestamps.
4. Run `python main.py --pdf_folder path/to/you/pdfs --video_folder your/video/folder --video_map path/to/video_map.pkl`
5. Enter your search string and hit Enter.
6. Use the arrow keys to navigate the results. Hit Enter to view the pdf at the location of the found text. Hit `v` to open the video corresponding to the result at the fitting timestamp.
7. If the timestamps don't line up perfectly or you want to jump into the videos a little earlier, you can try to fix it by adding a value to the --page_offset or --second_offset argument of `main.py`