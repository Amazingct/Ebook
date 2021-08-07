#!/usr/bin/python3
import os
import Books2Text as BB
from gtts import gTTS
import threading as t
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
import vlc
import time
page = 0
play_page = 0
file = ""
titleb= ""
pause = 0
main=tk.Tk()
p = vlc.MediaPlayer()


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


def play(stop=0):
    global titlep, p, pause, play_page
    if stop == 1:
        try:
            p.stop()
            title.config(text="STOPPED")
        except:
           print("stop not possible")
    else:
        content = viewer.get(1.0, END)
        if not(titlep+".mp3" in os.listdir("audio")):
            print("audio not found, creating audio")
            title.config(text="CONVERTING....")
            tts = gTTS(text=content, lang='en')
            tts.save("audio"+"/"+titlep+'.mp3')
            play_page = page
        if p.is_playing() == 1 and page==play_page:
            p.pause()
            pause = 1
            print("Paused...")
            title.config(text="PAUSED")
        elif p.is_playing() == 1 and not  page==play_page:
            p.stop()
            play_page=page
            p = vlc.MediaPlayer("audio"+"/"+titlep+'.mp3')
            p.play()
            pause = 0
            print("playing....")
            title.config(text="PLAYING....")
        elif pause == 1: # if it is paused
            p.play()
            pause=0
            print("resume..")
            title.config(text="PLAYING....")

        else: #not playing and wasnt paused
            play_page=play
            p = vlc.MediaPlayer("audio"+"/"+titlep+'.mp3')
            p.play()
            pause = 0
            print("playing....")
            title.config(text="PLAYING....")




def load_book():
    global viewer, page, titleb, titlep
    global book
    book = BB.Book(file)
    page = 0
    titleb = book.title
    titlep = titleb + str(page)
    txt = book.text[page]
    viewer.delete(1.0, END)
    viewer.insert(END, txt)
    title.config(text=titleb)


def previous_p():
    global page, viewer,titleb,titlep,book
    if not page <= 0:
        page = page - 1
        print ("page", page)
        viewer.delete(1.0, END)
        viewer.insert(tk.INSERT, book.text[page])
        titlep = titleb + str(page)

def next_p():
    global page, viewer, titlep, titleb,book
    if not page >= len(book.text)-1:
        page = page + 1
        titlep = titleb + str(page)
        print("page", page)
        viewer.delete(1.0, END)
        viewer.insert(tk.INSERT, book.text[page])


def buttons():
    while 1:
        presses = { "play": GPIO.input(25), "next": GPIO.input(12), "previous": GPIO.input(24)}
        if presses["previous"] == 0 and presses["next"] == 0:
            play(1)
        elif presses["play"] == 0:
            play()
        elif presses["next"] == 0:
            next_p()
        elif presses["previous"] == 0:
            previous_p()
        time.sleep(0.15)
 

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
#b_play = Button(main, text = 'PLAY', bg='ivory2', width = 10, command =play).pack(side=TOP)
#b_stop = Button(main, text = 'STOP', bg='ivory2', width = 10, command =play).pack(side=TOP)


t.Thread(target=buttons).start()
app=FullScreenApp(main)
main.mainloop()
