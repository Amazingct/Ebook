import Books2Text as BB
from gtts import gTTS
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
import vlc
main = Tk()
page = 0
file = ""

main.title("EBOOK READER")
main.geometry('800x400')
main.configure(background='ivory3')

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
        print ("page", page)
        viewer.delete(1.0, END)
        viewer.insert(tk.INSERT, book.text[page])

def next_p():
    global page, viewer
    if not page >= len(book.text)-1:
        page = page + 1
        print("page", page)
        viewer.delete(1.0, END)
        viewer.insert(tk.INSERT, book.text[page])

def stop():
    pass

def play():
    content = viewer.get(1.0, END)
    tts = gTTS(text=content, lang='en')
    tts.save('file.mp3')
    print(content)
    p = vlc.MediaPlayer("file.mp3")
    p.play()


def select_file():
    global file
    file = filedialog.askopenfilename(initialdir="/home/amazing/Documents/pythonProject/books", title="Select file",
                                      filetypes=(("pdf files", "*.pdf"), ("epub files", "*.epub"),  ("all files", "*.*")))
    load_book()


# file select
title = Label(main, text = 'BOOK NOT SELECTED:').pack(side=TOP)
b_select = Button(main, text = 'SELECT', bg='ivory2', width = 10, command =select_file).pack(side=TOP)

# page viewer
viewer = scrolledtext.ScrolledText(main, width=50, height=15)
viewer.pack(side=BOTTOM)
viewer.config(background="light grey", foreground="black", font='times 12 bold', wrap='word')

# buttons
b_play = Button(main, text = 'PLAY', bg='ivory2', width = 10, command =play).pack(side=TOP)
b_stop = Button(main, text = 'STOP', bg='ivory2', width = 10, command =stop).pack(side=TOP)
b_previous_page = Button(main, text = 'PREVIOUS', bg='ivory2', width = 10, command =previous_p).pack(side=TOP)
b_next_page = Button(main, text = 'NEXT', bg='ivory2', width = 10, command =next_p).pack(side=TOP)


main.mainloop()
