#! /usr/bin/env python3

# -=-=- Imports & Globals & Constants -=-=- #

import tkinter as tk
import threading


option_labels = (None, None, None, None)

# -=-=- Classes -=-=- #


# -=-=- Functions -=-=- #

def click_button(num, label):
    def _click_button():
        print(f"clicked button {num}")
        if label is not None:
            label['text'] = f"New Option {num}"
    
    return _click_button

def build_line_option(master, id):
    frame = tk.Frame(master)

    lbl = tk.Label(frame, text=f"Option {id+1}")
    btn = tk.Button(frame, text=f"Button {id+1}", command=click_button(id+1, lbl))
    
    btn.pack(side='left')
    lbl.pack(side='left')

    return frame

def build(root):
    frame = tk.Frame(root)
    
    build_line_option(frame, 0).pack()
    build_line_option(frame, 1).pack()
    build_line_option(frame, 2).pack()
    build_line_option(frame, 3).pack()

    frame.pack(side='left')

## -=-=- Entry Point -=-=- ##

def run():
    root = tk.Tk()
    build(root)
    root.mainloop()

def runThread():
    run()


## EOF
