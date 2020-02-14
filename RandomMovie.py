# -*- coding: utf8 -*-
import random
from tkinter import *
import tkinter as tk
from trakt import init
from trakt.users import User
from trakt.movies import Movie
from urllib.request import urlopen
from PIL import Image, ImageTk
from io import BytesIO
import requests
import imdb
import tkinter.simpledialog
# PopUp Kullanıcı Adı
popup = tk.Tk()
popup.withdraw()
username = tk.simpledialog.askstring("Trakt.TV", "   Please Enter Your Trakt.TV Username:   ")
if username is None:
    quit()
else:
    if username is "":
        username = tk.simpledialog.askstring("Empty Value", "           Please Enter An Valid Username:          ")
        if username is None:
            quit()
        else:
            if username is "":
                quit()
popup.destroy()
## IMDB, Trakt.TV Tanımları
moviesDB = imdb.IMDb()
my = User(str('lunedor'))
## Trakt.tv Watchlist Alımı
watchlist = my.watchlist_movies
# Veri İşlemleri
def callback():
    ### Terimler
    myline = str(random.choice(watchlist))[9:1000]
    movies = moviesDB.search_movie(str(myline))
    id = movies[0].getID()
    movie = moviesDB.get_movie(id)
    title = movie['title']
    year = movie["year"]
    rating = movie["rating"]
    runtimes = movie["runtimes"]
    runtime = ' '.join(map(str, runtimes))
    directors = movie["directors"]
    directStr = ' '.join(map(str, directors))
    writers = movie["writers"]
    writerStr = ', '.join(map(str, writers))
    casting = movie["cast"]
    actors = ', '.join(map(str, casting))
    summary = movie["plot outline"]
    genres = movie["genres"]
    genre = ', '.join(map(str, genres))
    posterurl = movie["full-size cover url"]
    ##Metin Ayarları
    global showline
    showline = title + "\n" + str(year) + " - " + str(rating) + "\n" + str(runtime) +" minutes" + " - " + genre
    global showline2
    showline2 = "Director: " + directStr + "\n" + "\n" + "Writers: " + writerStr + "\n" + "\n" + "Cast: " + actors[:100] + "..." + "\n" + "\n" + "Summary: " + "\n" + str(summary)
    ## Image Dosyası
    url = posterurl
    r = requests.get(url)
    global photo
    im= Image.open(BytesIO(r.content))
    MAX_SIZE = (200, 270)
    im.thumbnail(MAX_SIZE)
    photo = ImageTk.PhotoImage(im)
# GUI İşlemleri
def guishow():
    # GUI Veri Ayarları
    global posterframe
    posterframe.destroy()
    posterframe = tk.Label(image=photo)
    posterframe.image = photo
    posterframe.place(x=3, y=85)
    ## Metin Tasarım
    toptext.delete('1.0', END)
    toptext.insert("1.0", showline)
    toptext.tag_add('center', "1.0", "end")
    toptext.tag_configure("center", justify='center', font='Calibri 11 bold')
    righttext.delete('1.0', END)
    righttext.insert("1.0", showline2)
    righttext.tag_add('center', "1.0", "end")
    righttext.tag_configure("center", justify='left', font='Calibri 10 bold')
# Pencere oluşturma
mainwindow = Tk()
mainwindow.title("Pick A Movie For Me")
mainwindow.geometry("435x435")
mainwindow.configure(background='black')
# Poster için Frame oluşturma
posterframe = Frame(mainwindow)
posterframe.place(x=0, y=80)
posterframe.configure(background='black')
# Üst Yazı Alanı oluşturma
toptext = Text(mainwindow, height=4, width=54, wrap=WORD)
toptext.configure(background='snow2')
toptext.place(x=1, y=1)
# Sağ Yazı Alanı oluşturma
righttext = Text(mainwindow, height=17, width=27, wrap=WORD)
righttext.configure(background='ivory2')
righttext.place(x=210, y=83)
# Buton Fonksiyonları
def buttoncase():
    callback()
    guishow()
# Butonlar
b = Button(mainwindow, text="Good Luck!", command=buttoncase)
b.configure(background='gray18', foreground='white')
b.place(x=180, y=370)
c = Button(mainwindow, text="     Close     ", command=mainwindow.quit)
c.configure(background='gray18', foreground='white')
c.place(x=180, y=400)
mainloop()