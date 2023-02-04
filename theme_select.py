from os import system
import json
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle



key = None


### THEMED DEFAULTS ###

MAX_SIZE_W = 800
MAX_SIZE_H = 480


PADX_VERY_BIG = 275
PADX_BIG = 25
PADX = 10
PADY = 10
PADY_SHIFT = 25
WIDTH_B = 8

text_COL = 0
text_PADX = WIDTH_B * text_COL 
text_PADY = 10

### SELECTIONS ###
S_THEME    = ''
S_VOICE    = ''
S_MODIFIER = ''

### FIELD ###
FIELD = ''

### COLORS ###
BG_COLOR = ''
B2_COLOR = '' 
FG_COLOR = ''


# showing all data in display
exp = ""
is_shift = False


def display_menu(theme, voice, modifier):
    global S_THEME
    global S_VOICE
    global S_MODIFIER
    
    if theme == '':
        S_THEME = 'lightgreen'
        theme = S_THEME
        
    if voice == '':
        S_VOICE = '0'
    else:
        S_VOICE = voice
    if modifier == '':
        S_MODIFIER ='0'
    else:
        S_MODIFIER = modifier
    
    display(theme)

def save():

    try:
        FILE = open("/home/pi/Desktop/BMO/user_data.json", "r")
        JSON = json.load(FILE)
        FILE.close()
        
        
        JSON['theme']          = S_THEME
        JSON['voice_modifier'] = S_MODIFIER
        JSON['voice']          = S_VOICE
        
        print('THEME: ' + JSON['theme'])
        print('VOICE MODIFIER: ' + JSON['voice_modifier'])
        print('VOICE: ' + JSON['voice'])
        
        FILE = open("/home/pi/Desktop/BMO/user_data.json", "w")
        json.dump(JSON, FILE)
        FILE.close()

    except Exception as e:
        print(e)
    
    key.destroy()

def change_colors(theme):
    global BG_COLOR
    global B2_COLOR
    global FG_COLOR

    if theme == 'lightgreen':
        BG_COLOR = '#d7f5d1'
        B2_COLOR = '#e4f7df'
        FG_COLOR = '#90c49f'
    elif theme == 'rosepurple':
        BG_COLOR = '#efd1f5'
        B2_COLOR = '#f2dff7'
        FG_COLOR = '#c490b5'
    elif theme == 'autumnorange':
        BG_COLOR = '#fdda6e'
        B2_COLOR = '#ffdc95'
        FG_COLOR = '#f9b168'

def test_sound(voice, modifier):
    
    print('S_VOICE: ' + S_VOICE)
    if S_VOICE == '0':
        if S_MODIFIER == '0':
            BMO_voice = ' pitch +540 tempo -s 1.70 speed 0.82 treble +6 gain -B +1'
        if S_MODIFIER == '1':
            BMO_voice = ''
        system('gtts-cli "This is my voice." | play -t mp3 -' + BMO_voice)
    elif S_VOICE == '1':
        import pyttsx3
        voice_engine = pyttsx3.init()
        #voices = voice_engine.getProperty('voices')
        #voice_engine.setProperty('voice', voices[1].id)
        voice_engine.setProperty('rate', 100)  
        voice_engine.say('This is my voice.')
        voice_engine.runAndWait()
        voice_engine.stop()
    elif S_VOICE == '2':
        system('echo "This is my voice." | festival --tts') 

def set_VM(voice_id, modifier_id):
    global S_VOICE    
    global S_MODIFIER
    
    S_VOICE    = voice_id
    S_MODIFIER = modifier_id
    
    test_sound(S_VOICE, S_MODIFIER)

def set_T(theme, f, style):
    global S_THEME
    S_THEME    = theme
    
    change_colors(theme)
    
    f.config(background=BG_COLOR)
    key.configure(bg=BG_COLOR)
    style.configure('TButton', background=B2_COLOR)  
    style.configure('TButton', foreground=FG_COLOR)
    style.configure('TEntry', background=BG_COLOR)
    style.configure('TEntry', foreground=FG_COLOR)
    style.configure('TEntry', bordercolor=BG_COLOR)
    
    

def show_buttons(key, f, style):
    stuff_up = ttk.Entry(f, state='disabled', width=47, textvariable=up_text, justify='center', font=('Tw Cen MT Condensed Extra Bold', 18, 'bold'))
    up_text.set('Voice')
    stuff_up.grid(rowspan=1, column=0, columnspan=14, ipadx=text_PADX, ipady=text_PADY, pady=8)
    
    voice1_v1 = ttk.Button(f, text='gTTS 1', width=WIDTH_B+4, command=lambda: set_VM('0', '0'))
    voice1_v1.grid(row=1, column=4, ipadx=0, ipady=PADY, columnspan=3)
    voice1_v2 = ttk.Button(f, text='gTTS 2', width=WIDTH_B+4, command=lambda: set_VM('0', '1'))
    voice1_v2.grid(row=1, column=7, ipadx=0, ipady=PADY, columnspan=3)

    voice2_v1 = ttk.Button(f, text='pyTTSX 1', width=WIDTH_B*2+7, command=lambda: set_VM('1', '0'))
    voice2_v1.grid(row=2, column=0, ipadx=PADX, ipady=PADY, columnspan=15)
        
    voice3_v1 = ttk.Button(f, text='Festival 1', width=WIDTH_B*2+7, command=lambda: set_VM('2', '0'))
    voice3_v1.grid(row=3, column=0, ipadx=PADX, ipady=PADY, columnspan=15)
    
    stuff_down = ttk.Entry(f, state='disabled', width=47, textvariable=down_text, justify='center', font=('Tw Cen MT Condensed Extra Bold', 18, 'bold'))
    down_text.set('Theme')
    stuff_down.grid(row=4, column=0, columnspan=14, ipadx=text_PADX, ipady=text_PADY, pady=8)
    
    theme1 = ttk.Button(f, text='Lightgreen', width=WIDTH_B*2+2, command=lambda: set_T('lightgreen', f, style))
    theme1.grid(row=5, column=1, ipadx=0, ipady=PADY, columnspan=4, pady=8)
    
    theme2 = ttk.Button(f, text='Rosepurple', width=WIDTH_B*2+2, command=lambda: set_T('rosepurple', f, style))
    theme2.grid(row=5, column=5, ipadx=0, ipady=PADY, columnspan=4, pady=8)
    
    theme3 = ttk.Button(f, text='Autumnorange', width=WIDTH_B*2+2, command=lambda: set_T('autumnorange', f, style))
    theme3.grid(row=5, column=9, ipadx=0, ipady=PADY, columnspan=4, pady=8)
    
    
    save_btn = ttk.Button(f, text='SAVE', width=WIDTH_B*2, command=lambda: save())
    save_btn.grid(row=7, column=0, ipadx=PADX, ipady=PADY, columnspan=14, rowspan=2, pady=4)

    key.mainloop()
        
    #key.columnconfigure(0, weight=1)
    #key.rowconfigure(0, weight=1)
    #key.mainloop()
        

def display(theme):

    global key
    global up_text
    global down_text
    
    key = tk.Tk()

    key.geometry('800x480')  # Window size
    key.maxsize(width=MAX_SIZE_W, height=MAX_SIZE_H)
    key.minsize(width=MAX_SIZE_W, height=MAX_SIZE_H)

    key.attributes('-topmost',True)
    key.attributes("-fullscreen", True)
    
    w, h = key.winfo_screenwidth(), key.winfo_screenheight()
    key.overrideredirect(1)
    key.overrideredirect(0)

    key.focus_set()
    key.bind("<Escape>", lambda event:key.destroy())
    
    #COLORS
    #90c49f
    #d7f5d1
    #e4f0df
    
    change_colors(theme)
    
    f = tk.Frame(key, background=BG_COLOR)
    f.config(background=BG_COLOR)       
    f.grid(row=0, column=0)

    style = ThemedStyle(key)
    style.theme_use('adapta')

    
    key.configure(bg=BG_COLOR)
    style.configure('TButton', background=B2_COLOR)  
    style.configure('TButton', foreground=FG_COLOR)  
    style.configure('TButton', font=('Tw Cen MT Condensed Extra Bold', 14, 'bold'))
    style.configure('TEntry', background=BG_COLOR)
    style.configure('TEntry', foreground=FG_COLOR)
    style.configure('TEntry', bordercolor=BG_COLOR)

    up_text = tk.StringVar()
    down_text = tk.StringVar()
    
    #style.configure('TEntry', fieldbackground='red', bordercolor=BG_COLOR, background=BG_COLOR, foreground=FG_COLOR) # entry box
    #equation = tk.StringVar()
    #Dis_entry = ttk.Entry(f, state='disabled', textvariable=equation, background=BG_COLOR, foreground=FG_COLOR, justify='center', font=('Tw Cen MT Condensed Extra Bold', 18, 'bold'))
    #Dis_entry.grid(rowspan=1, column=text_COL, columnspan=14-text_COL*2, ipadx=text_PADX, ipady=text_PADY, pady=12)

    #equation.set(placeholder)

    show_buttons(key, f, style)


