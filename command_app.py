import urwid
import subprocess
import os,sys
import pickle

with open("slide_second_map.pkl","rb") as f:
    video_map = pickle.load(f)
with open("slide_map.pkl","rb") as f:
    slide_map = pickle.load(f)

glob_currently_selected = None
glob_list_box = None
glob_choices = None

def exit_on_q(key):
    if key in ["q","Q"]:
        raise urwid.ExitMainLoop()  
    if key in ["v","V"]:
        open_video(os.path.basename(glob_currently_selected[0]),int(glob_currently_selected[1]))

def open_video(pdf,page_num):
    real_page_num = slide_map[(pdf,page_num)]
    slides_num = int(pdf.split("-")[0])
    for pnum in range(real_page_num,0,-1):
        key = (slides_num,pnum)
        if key in video_map:
            video = video_map[key][0]
            if pnum == real_page_num:
                timestamp = video_map[key][1][0]
            else:
                timestamp = video_map[key][1][1]
            break
    subprocess.run(["vlc",f"--start-time={timestamp}",os.path.join("videos",f"Folien-{slides_num}",video)],stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def program_main(pdfpath):
    while 1:
        search_string = ""
        while search_string.strip()=="":
            search_string = input("Search for text in pdfs.\n")
        with open(".tmp.txt", "w") as f:
            subprocess.run(["pdfgrep", "-i","-R", "-n", "--cache", search_string,pdfpath],stdout=f)
        with open(".tmp.txt", "r") as f:
            prechoices = [[y.strip() for y in x.split(":")[:2]+[":".join(x.split(":")[2:])]] for x in f.read().splitlines()]
        
        choices = []
        for choice in prechoices:
            index = choice[2].lower().find(search_string.lower())
            if index!=-1:
                choices.append([choice[0],choice[1],choice[2][:index],choice[2][index:index+len(search_string)],choice[2][index+len(search_string):]])

        if len(choices) == 0:
            print("No Results Found")
            continue

        main = urwid.Padding(menu(u'Results', choices), left=2, right=2)
        top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align='center', width=('relative', 100),
            valign='middle', height=('relative', 100),
            min_width=20, min_height=9)
        urwid.MainLoop(top, palette=[('reversed', 'white', ''),("blue", "dark blue", ''),
                                     ("magenta","dark magenta",""),("white","white",""),
                                     ("red","light red","")],unhandled_input=exit_on_q).run()

def open_file(button, choice):
    subprocess.run(["evince","-i",choice[1],choice[0]])    

def test_callback():
    global glob_currently_selected
    index = int(str(glob_list_box.get_focus()[1]))-2
    glob_currently_selected = glob_choices[index]

def menu(title, choices):
    global glob_list_box, glob_choices
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        button = urwid.Button([
            ("blue",(c[0]+" ").encode()),
            ("magenta",("Page "+c[1]+" ").encode()),
            ("white",(" " if c[2]=="" else c[2]).encode()),
            ("red",(c[3]).encode()),
            ("white",(" " if c[4]=="" else c[4]).encode()),
        ])
        urwid.connect_signal(button, 'click', open_file, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    walker = urwid.SimpleFocusListWalker(body)
    urwid.connect_signal(walker, "modified", test_callback)
    list_box = urwid.ListBox(walker)
    glob_list_box = list_box
    glob_choices = choices
    return list_box

def exit_program(button):
    raise urwid.ExitMainLoop()

if __name__ == '__main__':
    program_main(sys.argv[1] if len(sys.argv)>1 else "folien")