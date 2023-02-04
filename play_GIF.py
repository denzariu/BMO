import tkinter as tk
from PIL import Image, ImageTk
from itertools import count
from sys import argv

root = tk.Tk()

filename = '/home/pi/Desktop/BMO/text_output.o'

spaces = '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
TEXT_TO_DISPLAY = tk.StringVar(root)
FONT_SIZE = '18'
FONT_TO_DISPLAY = 'Book\ Antiqua ' + FONT_SIZE + ' bold'

def getText():
    global FONT_SIZE, FONT_TO_DISPLAY
    
    with open(filename, 'r') as filehandle:
        text = filehandle.read()
        filehandle.close()
        text = text.replace('. ', '.\n').replace('? ', '?\n')
        leng = len(text)

        # max 72 per line at FS = 12 with '9'
        if leng > 61:
            spaces = '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
            FONT_SIZE = '12'
        elif leng > 53:
            spaces = '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
            FONT_SIZE = '14'
        elif leng > 44:
            spaces = '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
            FONT_SIZE = '16'
        else:
            spaces = '\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
            FONT_SIZE = '18'

        FONT_TO_DISPLAY = 'Book\ Antiqua ' + FONT_SIZE + ' bold'
        #print(FONT_TO_DISPLAY + ' ' + str(len(text)) + ' --- ' + text)
        TEXT_TO_DISPLAY.set(spaces + text)




class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []
        
        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        self.delay = 110

        
        if len(self.frames) == 1:
            self.frames[0] = ImageTk.PhotoImage(im.copy().resize((int(480*im.width/im.height), 480), Image.ANTIALIAS))
            self.update_text()
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None
    
    def update_text(self):
        getText()
        self.config(image=self.frames[0], textvariable=TEXT_TO_DISPLAY, font=FONT_TO_DISPLAY, compound='center')
        self.after(self.delay * 15, self.update_text)
    
    def next_frame(self):
        if self.loc == 0:
            getText()
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc], textvariable=TEXT_TO_DISPLAY, font=FONT_TO_DISPLAY, compound='center')
            self.after(self.delay, self.next_frame)
    

lbl = ImageLabel(root)
lbl.config(bg=argv[3])
lbl.pack()

###
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.overrideredirect(0)

#root.configure(bg=argv[3]) 
root['bg'] = argv[3]


root.attributes("-fullscreen", True)
root.wm_attributes("-topmost", 1)

#root.geometry("%dx%d+0+0" % (w, h))
root.focus_set()
root.bind("<Escape>", lambda event:root.destroy())

#root.after(5000, root.destroy)
###

lbl.load('/home/pi/Desktop/BMO/Assets/' + argv[1] + "." + argv[2])
root.mainloop()
