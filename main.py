#!/usr/bin/python3
import Books2Text as BB
from gtts import gTTS
import threading as t
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
import vlc
page = 0
file = ""
main=tk.Tk()

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)

    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom



import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)



main.title("EBOOK READER")
main.geometry('900x300')
main.configure(background='ivory3')


def play():
    global title
    content = viewer.get(1.0, END)
    tts = gTTS(text=content, lang='en')
    tts.save('file.mp3')
    p = vlc.MediaPlayer("file.mp3")
    if p.is_playing() == 1:
        p.stop()
        title.config(text="STOPPING...")
    else:
        p.play()
        title.config(text="PLAYING....")

def load_book():
    global viewer, page
    global book
    book = BB.Book(file)
    page = 0
    txt = book.text[page]
    viewer.delete(1.0, END)
    viewer.insert(END, txt)
    title.config(text=file)


def previous_p():
    global page, viewer
    if not page <= 0:
        page = page - 1
       # print ("page", page)
        viewer.delete(1.0, END)
        viewer.insert(tk.INSERT, book.text[page])

def next_p():
    global page, viewer
    if not page >= len(book.text)-1:
        page = page + 1
        #print("page", page)
        viewer.delete(1.0, END)
        viewer.insert(tk.INSERT, book.text[page])



def buttons():
    while 1:
        presses = { "play": GPIO.input(25), "next": GPIO.input(12), "previous": GPIO.input(24)}
        if presses["play"] == 0:
            play()
        elif presses["next"] == 0:
            next_p()
        elif presses["previous"] == 0:
            previous_p()


def select_file():
    global file
    file = filedialog.askopenfilename(initialdir="/home/amazing/Documents/pythonProject/books", title="Select file",
                                      filetypes=(("pdf files", "*.pdf"), ("epub files", "*.epub"),  ("all files", "*.*")))
    load_book()

# file select
title = Label(main, text = 'BOOK NOT SELECTED:')
title.pack(side=TOP)
b_select = Button(main, text = 'SELECT', bg='ivory2', width = 10, command =select_file).pack(side=TOP)

# page viewer
viewer = scrolledtext.ScrolledText(main, width=100, height=20)
viewer.pack(side=TOP)
viewer.config(background="light grey", foreground="black", font='times 12 bold', wrap='word')

# buttons
# b_play = Button(main, text = 'PLAY', bg='ivory2', width = 10, command =play).pack(side=TOP)
# b_stop = Button(main, text = 'STOP', bg='ivory2', width = 10, command =stop).pack(side=TOP)


t.Thread(target=buttons).start()
app=FullScreenApp(main)
main.mainloop()