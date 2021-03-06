import urwid
import subprocess
import os,sys

def exit_on_q(key):
    if key in ["q","Q"]:
        raise urwid.ExitMainLoop()        

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

def menu(title, choices):
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
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def exit_program(button):
    raise urwid.ExitMainLoop()

if __name__ == '__main__':
    try:
        program_main(sys.argv[1] if len(sys.argv)>1 else "folien")
    except:
        try:
            os.remove(".tmp.txt")
            pass
        except:
            pass