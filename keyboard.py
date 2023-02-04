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
PADX = 0
PADY = 3
PADY_SHIFT = 25
WIDTH_B = 2

text_COL = 0
text_PADX = WIDTH_B * text_COL 
text_PADY = 10

global placeholder
placeholder = 'Press any key...'

### FIELD ###
FIELD = ''

# Input string
exp = ""

# Uppercase / Lowercase check
is_shift = False

# Set JSON Field to modify
def set_field(_field):
    global FIELD
    FIELD = _field

# This might be confusing but is needed for a reason I don't remember right now 
# (maybe has a more suggestive name to be referenced from main)
def display_keyboard(theme):
    display(theme)

# Push data to JSON
def Enter(equation):
    global exp

    try:
        FILE = open("/home/pi/Desktop/BMO/user_data.json", "r")
        JSON = json.load(FILE)
        FILE.close()

        FILE = open("/home/pi/Desktop/BMO/user_data.json", "w")
        print(exp + '--------------------')
        JSON[FIELD] = exp
        print(JSON[FIELD])
        json.dump(JSON, FILE)
        FILE.close()

    except Exception as e:
        print(e)

    Clear(equation)
    key.destroy()

# Add characters to current input
def press(num, equation):
    global exp
    exp = exp + str(num)
    equation.set(exp)

# Autofill input from existing JSON
def autofill(equation):
    global exp
    FILE = open("/home/pi/Desktop/BMO/user_data.json", "r")
    JSON = json.load(FILE)
    FILE.close()
    exp = JSON[FIELD]
    equation.set(exp)

# Clear last character
def Backspace(equation):
    global exp
    exp = exp[:-1]
    equation.set(exp)

# Uppercase / lowercase switch
def Shift(key, f, equation):
    global is_shift
    is_shift = not is_shift
    switch_keyboard(key, f, equation)

# Clear all characters from input
def Clear(equation):
    global exp, placeholder
    exp = ""
    equation.set(placeholder)

# Keyboard display (after configuration)
def switch_keyboard(key, f, equation):
    if (is_shift):
        # Adding keys line wise
        # First Line Button
        tilda = ttk.Button(f, text='~', width=WIDTH_B, command=lambda: press('~', equation))
        tilda.grid(row=1, column=0, ipadx=PADX, ipady=PADY)

        num1 = ttk.Button(f, text='!', width=WIDTH_B, command=lambda: press('!', equation))
        num1.grid(row=1, column=1, ipadx=PADX, ipady=PADY)

        num2 = ttk.Button(f, text='@', width=WIDTH_B, command=lambda: press('@', equation))
        num2.grid(row=1, column=2, ipadx=PADX, ipady=PADY)

        num3 = ttk.Button(f, text='#', width=WIDTH_B, command=lambda: press('#', equation))
        num3.grid(row=1, column=3, ipadx=PADX, ipady=PADY)

        num4 = ttk.Button(f, text='$', width=WIDTH_B, command=lambda: press('$', equation))
        num4.grid(row=1, column=4, ipadx=PADX, ipady=PADY)

        num5 = ttk.Button(f, text='%', width=WIDTH_B, command=lambda: press('%', equation))
        num5.grid(row=1, column=5, ipadx=PADX, ipady=PADY)

        num6 = ttk.Button(f, text='^', width=WIDTH_B, command=lambda: press('^', equation))
        num6.grid(row=1, column=6, ipadx=PADX, ipady=PADY)

        num7 = ttk.Button(f, text='&', width=WIDTH_B, command=lambda: press('&', equation))
        num7.grid(row=1, column=7, ipadx=PADX, ipady=PADY)

        num8 = ttk.Button(f, text='*', width=WIDTH_B, command=lambda: press('*', equation))
        num8.grid(row=1, column=8, ipadx=PADX, ipady=PADY)

        num9 = ttk.Button(f, text='(', width=WIDTH_B, command=lambda: press('(', equation))
        num9.grid(row=1, column=9, ipadx=PADX, ipady=PADY)

        num0 = ttk.Button(f, text=')', width=WIDTH_B, command=lambda: press(')', equation))
        num0.grid(row=1, column=10, ipadx=PADX, ipady=PADY)

        under = ttk.Button(f, text='_', width=WIDTH_B, command=lambda: press('_', equation))
        under.grid(row=1, column=11, ipadx=PADX, ipady=PADY)

        plus = ttk.Button(f, text='+', width=WIDTH_B, command=lambda: press('+', equation))
        plus.grid(row=1, column=12, ipadx=PADX, ipady=PADY)

        backspace = ttk.Button(
            f, text='←', width=WIDTH_B, command=lambda: Backspace(equation))
        backspace.grid(row=1, column=13, ipadx=PADX, ipady=PADY)

        # Second Line Buttons

        Q = ttk.Button(f, text='Q', width=WIDTH_B, command=lambda: press('Q', equation))
        Q.grid(row=2, column=2, ipadx=PADX, ipady=PADY)

        W = ttk.Button(f, text='W', width=WIDTH_B, command=lambda: press('W', equation))
        W.grid(row=2, column=3, ipadx=PADX, ipady=PADY)

        E = ttk.Button(f, text='E', width=WIDTH_B, command=lambda: press('E', equation))
        E.grid(row=2, column=4, ipadx=PADX, ipady=PADY)

        R = ttk.Button(f, text='R', width=WIDTH_B, command=lambda: press('R', equation))
        R.grid(row=2, column=5, ipadx=PADX, ipady=PADY)

        T = ttk.Button(f, text='T', width=WIDTH_B, command=lambda: press('T', equation))
        T.grid(row=2, column=6, ipadx=PADX, ipady=PADY)

        Y = ttk.Button(f, text='Y', width=WIDTH_B, command=lambda: press('Y', equation))
        Y.grid(row=2, column=7, ipadx=PADX, ipady=PADY)

        U = ttk.Button(f, text='U', width=WIDTH_B, command=lambda: press('U', equation))
        U.grid(row=2, column=8, ipadx=PADX, ipady=PADY)

        I = ttk.Button(f, text='I', width=WIDTH_B, command=lambda: press('I', equation))
        I.grid(row=2, column=9, ipadx=PADX, ipady=PADY)

        O = ttk.Button(f, text='O', width=WIDTH_B, command=lambda: press('O', equation))
        O.grid(row=2, column=10, ipadx=PADX, ipady=PADY)

        P = ttk.Button(f, text='P', width=WIDTH_B, command=lambda: press('P', equation))
        P.grid(row=2, column=11, ipadx=PADX, ipady=PADY)

        # Third Line Buttons

        A = ttk.Button(f, text='A', width=WIDTH_B, command=lambda: press('A', equation))
        A.grid(row=3, column=2, ipadx=PADX, ipady=PADY)

        S = ttk.Button(f, text='S', width=WIDTH_B, command=lambda: press('S', equation))
        S.grid(row=3, column=3, ipadx=PADX, ipady=PADY)

        D = ttk.Button(f, text='D', width=WIDTH_B, command=lambda: press('D', equation))
        D.grid(row=3, column=4, ipadx=PADX, ipady=PADY)

        F = ttk.Button(f, text='F', width=WIDTH_B, command=lambda: press('F', equation))
        F.grid(row=3, column=5, ipadx=PADX, ipady=PADY)

        G = ttk.Button(f, text='G', width=WIDTH_B, command=lambda: press('G', equation))
        G.grid(row=3, column=6, ipadx=PADX, ipady=PADY)

        H = ttk.Button(f, text='H', width=WIDTH_B, command=lambda: press('H', equation))
        H.grid(row=3, column=7, ipadx=PADX, ipady=PADY)

        J = ttk.Button(f, text='J', width=WIDTH_B, command=lambda: press('J', equation))
        J.grid(row=3, column=8, ipadx=PADX, ipady=PADY)

        K = ttk.Button(f, text='K', width=WIDTH_B, command=lambda: press('K', equation))
        K.grid(row=3, column=9, ipadx=PADX, ipady=PADY)

        L = ttk.Button(f, text='L', width=WIDTH_B, command=lambda: press('L', equation))
        L.grid(row=3, column=10, ipadx=PADX, ipady=PADY)

        colon = ttk.Button(f, text=':', width=WIDTH_B,
                           command=lambda: press(':', equation))
        colon.grid(row=3, column=11, ipadx=PADX, ipady=PADY)

        quotation = ttk.Button(f, text='"', width=WIDTH_B,
                               command=lambda: press('"', equation))
        quotation.grid(row=3, column=12, ipadx=PADX, ipady=PADY)

        pipe = ttk.Button(f, text='|', width=WIDTH_B, command=lambda: press('|', equation))
        pipe.grid(row=3, column=13, ipadx=PADX, ipady=PADY)

        clear = ttk.Button(f, text='Clear', width=WIDTH_B, command=lambda: Clear(equation))
        clear.grid(row=2, column=12, columnspan=2, ipadx=PADX_BIG, ipady=PADY)

        enter = ttk.Button(f, text='Enter', width=WIDTH_B, command=lambda: Enter(equation))
        enter.grid(row=4, column=12, columnspan=2, rowspan=2, ipadx=PADX_BIG, ipady=PADY_SHIFT)

        # Fourth line Buttons

        shift = ttk.Button(f, text='▼', width=WIDTH_B, command=lambda: Shift(key, f, equation))
        shift.grid(row=3, column=0, columnspan=2, rowspan=2, ipadx=PADX_BIG, ipady=PADY_SHIFT)

        Z = ttk.Button(f, text='Z', width=WIDTH_B, command=lambda: press('Z', equation))
        Z.grid(row=4, column=2, ipadx=PADX, ipady=PADY)

        X = ttk.Button(f, text='X', width=WIDTH_B, command=lambda: press('X', equation))
        X.grid(row=4, column=3, ipadx=PADX, ipady=PADY)

        C = ttk.Button(f, text='C', width=WIDTH_B, command=lambda: press('C', equation))
        C.grid(row=4, column=4, ipadx=PADX, ipady=PADY)

        V = ttk.Button(f, text='V', width=WIDTH_B, command=lambda: press('V', equation))
        V.grid(row=4, column=5, ipadx=PADX, ipady=PADY)

        B = ttk.Button(f, text='B', width=WIDTH_B, command=lambda: press('B', equation))
        B.grid(row=4, column=6, ipadx=PADX, ipady=PADY)

        N = ttk.Button(f, text='N', width=WIDTH_B, command=lambda: press('N', equation))
        N.grid(row=4, column=7, ipadx=PADX, ipady=PADY)

        M = ttk.Button(f, text='M', width=WIDTH_B, command=lambda: press('M', equation))
        M.grid(row=4, column=8, ipadx=PADX, ipady=PADY)

        ang_l = ttk.Button(f, text='<', width=WIDTH_B, command=lambda: press('<', equation))
        ang_l.grid(row=4, column=9, ipadx=PADX, ipady=PADY)

        ang_r = ttk.Button(f, text='>', width=WIDTH_B, command=lambda: press('>', equation))
        ang_r.grid(row=4, column=10, ipadx=PADX, ipady=PADY)

        question = ttk.Button(f, text='?', width=WIDTH_B,
                              command=lambda: press('?', equation))
        question.grid(row=4, column=11, ipadx=PADX, ipady=PADY)

        # Fifth Line Buttons

        space = ttk.Button(f, text='Space', width=WIDTH_B,
                           command=lambda: press(' ', equation))
        space.grid(row=5, column=0, columnspan=12, ipadx=PADX_VERY_BIG, ipady=PADY)

        key.mainloop()

    else:
        # Adding keys line wise
        # First Line Button
        tick = ttk.Button(f, text='`', width=WIDTH_B, command=lambda: press('`', equation))
        tick.grid(row=1, column=0, ipadx=PADX, ipady=PADY)

        num1 = ttk.Button(f, text='1', width=WIDTH_B, command=lambda: press('1', equation))
        num1.grid(row=1, column=1, ipadx=PADX, ipady=PADY)

        num2 = ttk.Button(f, text='2', width=WIDTH_B, command=lambda: press('2', equation))
        num2.grid(row=1, column=2, ipadx=PADX, ipady=PADY)

        num3 = ttk.Button(f, text='3', width=WIDTH_B, command=lambda: press('3', equation))
        num3.grid(row=1, column=3, ipadx=PADX, ipady=PADY)

        num4 = ttk.Button(f, text='4', width=WIDTH_B, command=lambda: press('4', equation))
        num4.grid(row=1, column=4, ipadx=PADX, ipady=PADY)

        num5 = ttk.Button(f, text='5', width=WIDTH_B, command=lambda: press('5', equation))
        num5.grid(row=1, column=5, ipadx=PADX, ipady=PADY)

        num6 = ttk.Button(f, text='6', width=WIDTH_B, command=lambda: press('6', equation))
        num6.grid(row=1, column=6, ipadx=PADX, ipady=PADY)

        num7 = ttk.Button(f, text='7', width=WIDTH_B, command=lambda: press('7', equation))
        num7.grid(row=1, column=7, ipadx=PADX, ipady=PADY)

        num8 = ttk.Button(f, text='8', width=WIDTH_B, command=lambda: press('8', equation))
        num8.grid(row=1, column=8, ipadx=PADX, ipady=PADY)

        num9 = ttk.Button(f, text='9', width=WIDTH_B, command=lambda: press('9', equation))
        num9.grid(row=1, column=9, ipadx=PADX, ipady=PADY)

        num0 = ttk.Button(f, text='0', width=WIDTH_B, command=lambda: press('0', equation))
        num0.grid(row=1, column=10, ipadx=PADX, ipady=PADY)

        minus = ttk.Button(f, text='-', width=WIDTH_B, command=lambda: press('-', equation))
        minus.grid(row=1, column=11, ipadx=PADX, ipady=PADY)

        equal = ttk.Button(f, text='=', width=WIDTH_B, command=lambda: press('=', equation))
        equal.grid(row=1, column=12, ipadx=PADX, ipady=PADY)

        backspace = ttk.Button(
            f, text='←', width=WIDTH_B, command=lambda: Backspace(equation))
        backspace.grid(row=1, column=13, ipadx=PADX, ipady=PADY)

        # Second Line Buttons

        Q = ttk.Button(f, text='q', width=WIDTH_B, command=lambda: press('q', equation))
        Q.grid(row=2, column=2, ipadx=PADX, ipady=PADY)

        W = ttk.Button(f, text='w', width=WIDTH_B, command=lambda: press('w', equation))
        W.grid(row=2, column=3, ipadx=PADX, ipady=PADY)

        E = ttk.Button(f, text='e', width=WIDTH_B, command=lambda: press('e', equation))
        E.grid(row=2, column=4, ipadx=PADX, ipady=PADY)

        R = ttk.Button(f, text='r', width=WIDTH_B, command=lambda: press('r', equation))
        R.grid(row=2, column=5, ipadx=PADX, ipady=PADY)

        T = ttk.Button(f, text='t', width=WIDTH_B, command=lambda: press('t', equation))
        T.grid(row=2, column=6, ipadx=PADX, ipady=PADY)

        Y = ttk.Button(f, text='y', width=WIDTH_B, command=lambda: press('y', equation))
        Y.grid(row=2, column=7, ipadx=PADX, ipady=PADY)

        U = ttk.Button(f, text='u', width=WIDTH_B, command=lambda: press('u', equation))
        U.grid(row=2, column=8, ipadx=PADX, ipady=PADY)

        I = ttk.Button(f, text='i', width=WIDTH_B, command=lambda: press('i', equation))
        I.grid(row=2, column=9, ipadx=PADX, ipady=PADY)

        O = ttk.Button(f, text='o', width=WIDTH_B, command=lambda: press('o', equation))
        O.grid(row=2, column=10, ipadx=PADX, ipady=PADY)

        P = ttk.Button(f, text='p', width=WIDTH_B, command=lambda: press('p', equation))
        P.grid(row=2, column=11, ipadx=PADX, ipady=PADY)

        # Third Line Buttons
        autofill_last = ttk.Button(f, text='fill', width=WIDTH_B, command=lambda: autofill(equation))
        autofill_last.grid(row=2, column=0, ipadx=PADX_BIG, ipady=PADY, columnspan=2)

        A = ttk.Button(f, text='a', width=WIDTH_B, command=lambda: press('a', equation))
        A.grid(row=3, column=2, ipadx=PADX, ipady=PADY)

        S = ttk.Button(f, text='s', width=WIDTH_B, command=lambda: press('s', equation))
        S.grid(row=3, column=3, ipadx=PADX, ipady=PADY)

        D = ttk.Button(f, text='d', width=WIDTH_B, command=lambda: press('d', equation))
        D.grid(row=3, column=4, ipadx=PADX, ipady=PADY)

        F = ttk.Button(f, text='f', width=WIDTH_B, command=lambda: press('f', equation))
        F.grid(row=3, column=5, ipadx=PADX, ipady=PADY)

        G = ttk.Button(f, text='g', width=WIDTH_B, command=lambda: press('g', equation))
        G.grid(row=3, column=6, ipadx=PADX, ipady=PADY)

        H = ttk.Button(f, text='h', width=WIDTH_B, command=lambda: press('h', equation))
        H.grid(row=3, column=7, ipadx=PADX, ipady=PADY)

        J = ttk.Button(f, text='j', width=WIDTH_B, command=lambda: press('j', equation))
        J.grid(row=3, column=8, ipadx=PADX, ipady=PADY)

        K = ttk.Button(f, text='k', width=WIDTH_B, command=lambda: press('k', equation))
        K.grid(row=3, column=9, ipadx=PADX, ipady=PADY)

        L = ttk.Button(f, text='l', width=WIDTH_B, command=lambda: press('l', equation))
        L.grid(row=3, column=10, ipadx=PADX, ipady=PADY)

        semi_co = ttk.Button(f, text=';', width=WIDTH_B,
                             command=lambda: press(';', equation))
        semi_co.grid(row=3, column=11, ipadx=PADX, ipady=PADY)

        quotation = ttk.Button(f, text="'", width=WIDTH_B,
                               command=lambda: press('\'', equation))
        quotation.grid(row=3, column=12, ipadx=PADX, ipady=PADY)

        empty1 = ttk.Button(f, text='', width=WIDTH_B, command=lambda: press('', equation))
        empty1.grid(row=3, column=13, ipadx=PADX, ipady=PADY)

        enter = ttk.Button(f, text='Enter', width=WIDTH_B, command=lambda: Enter(equation))
        enter.grid(row=4, column=12, columnspan=2, rowspan=2, ipadx=PADX_BIG, ipady=PADY_SHIFT)

        # Fourth line Buttons

        shift = ttk.Button(f, text='▲', width=WIDTH_B, command=lambda: Shift(key, f, equation))
        shift.grid(row=3, column=0, columnspan=2, rowspan=2, ipadx=PADX_BIG, ipady=PADY_SHIFT)

        Z = ttk.Button(f, text='z', width=WIDTH_B, command=lambda: press('z', equation))
        Z.grid(row=4, column=2, ipadx=PADX, ipady=PADY)

        X = ttk.Button(f, text='x', width=WIDTH_B, command=lambda: press('x', equation))
        X.grid(row=4, column=3, ipadx=PADX, ipady=PADY)

        C = ttk.Button(f, text='c', width=WIDTH_B, command=lambda: press('c', equation))
        C.grid(row=4, column=4, ipadx=PADX, ipady=PADY)

        V = ttk.Button(f, text='v', width=WIDTH_B, command=lambda: press('v', equation))
        V.grid(row=4, column=5, ipadx=PADX, ipady=PADY)

        B = ttk.Button(f, text='b', width=WIDTH_B, command=lambda: press('b', equation))
        B.grid(row=4, column=6, ipadx=PADX, ipady=PADY)

        N = ttk.Button(f, text='n', width=WIDTH_B, command=lambda: press('n', equation))
        N.grid(row=4, column=7, ipadx=PADX, ipady=PADY)

        M = ttk.Button(f, text='m', width=WIDTH_B, command=lambda: press('m', equation))
        M.grid(row=4, column=8, ipadx=PADX, ipady=PADY)

        comma = ttk.Button(f, text=',', width=WIDTH_B, command=lambda: press(',', equation))
        comma.grid(row=4, column=9, ipadx=PADX, ipady=PADY)

        dot = ttk.Button(f, text='.', width=WIDTH_B, command=lambda: press('.', equation))
        dot.grid(row=4, column=10, ipadx=PADX, ipady=PADY)

        slash = ttk.Button(f, text='/', width=WIDTH_B, command=lambda: press('/', equation))
        slash.grid(row=4, column=11, ipadx=PADX, ipady=PADY)

        clear = ttk.Button(f, text='Clear', width=WIDTH_B, command=lambda: Clear(equation))
        clear.grid(row=2, column=12, columnspan=2, ipadx=PADX_BIG, ipady=PADY)

        # Fifth Line Buttons

        space = ttk.Button(f, text='Space', width=WIDTH_B,
                           command=lambda: press(' ', equation))
        space.grid(row=5, column=0, columnspan=12, ipadx=PADX_VERY_BIG, ipady=PADY)
        

        key.columnconfigure(0, weight=1)
        key.rowconfigure(0, weight=1)
        key.mainloop()
        

def display(theme):

    
    global key

    
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
    BG_COLOR = ''
    B2_COLOR = ''
    FG_COLOR = ''
    
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
    else:
        BG_COLOR = '#d7f5d1'
        B2_COLOR = '#e4f7df'
        FG_COLOR = '#90c49f'

    f = tk.Frame(key, background=BG_COLOR)
    f.grid(row=0, column=0)

    style = ThemedStyle(key)
    style.theme_use('adapta')


    f.config(background=BG_COLOR)
    key.configure(bg=BG_COLOR)
    style.configure('TButton', background=B2_COLOR)  
    style.configure('TButton', foreground=FG_COLOR)  
    style.configure('TButton', font=('Tw Cen MT Condensed Extra Bold', 14, 'bold'))


    style.configure('TEntry', fieldbackground='red', bordercolor=BG_COLOR) # entry box
    equation = tk.StringVar()
    Dis_entry = ttk.Entry(f, state='disabled', textvariable=equation, background=BG_COLOR, foreground=FG_COLOR, justify='center', font=('Tw Cen MT Condensed Extra Bold', 18, 'bold'))
    Dis_entry.grid(rowspan=1, column=text_COL, columnspan=14-text_COL*2, ipadx=text_PADX, ipady=text_PADY, pady=12)

    equation.set(placeholder)

    switch_keyboard(key, f, equation)




