import tkinter as tk
import pandas as pd

import os
import time

from PIL import ImageTk, Image
from edit import Edit
from add import Add
from gtts import gTTS
from pygame import mixer
from tkinter import messagebox

#App for learning english words
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.df = pd.read_csv('words.csv')
        self.__load_words(index=self.index)
        self.__create_app()
    #load_data
    def __load_words(self, index=0):
        self.word = self.df['word'][index]
        self.example = self.df['example'][index]
        self.meaning = self.df['meaning'][index]
        self.img_path = self.df['image'][index]
    #create app
    def __create_app(self, width=1100, height=800):
        self.geometry(f'{width}x{height}')
        self.title('English Words')
        icon = tk.PhotoImage(file='icon.png')
        self.iconphoto(False, icon)
        self.configure(bg='black')
        self.resizable(False, False)

        self.next_btn = self.__create_btn('->', self.__next_word, width-100, height-100)
        self.prev_btn = self.__create_btn('<-', self.__prev_word, 50, height-100)
        self.add_word_btn = self.__create_btn('Add Word', self.__add_word, width//2-300, height-100)
        self.edit_word_btn = self.__create_btn('Edit Word', self.__edit_word, width//2+100, height-100)
        self.search_btn = self.__create_btn('🔎', self.__search_word, width-140, 20, font=('Courier', 12))

        self.word_label = self.__create_label(f'Word: {self.word}', 50, height-400)
        self.btn_to_play_word = self.__create_btn('🎧', lambda: self.__play_sound(self.word), width-100, height-400, font=('Courier', 12))
        self.example_label = self.__create_label(f'Example: {self.example}', 50, height-300)
        self.btn_to_play_word = self.__create_btn('🎧', lambda: self.__play_sound(self.example), width-100, height-300, font=('Courier', 12))
        self.meaning_label = self.__create_label(f'Meaning: {self.meaning}', 50, height-200)
        self.btn_to_play_word = self.__create_btn('🎧', lambda: self.__play_sound(self.meaning), width-100, height-200, font=('Courier', 12))

        self.word_to_search = self.search_input = tk.Entry(self)
        self.word_to_search.place(x=width-300, y=23)


        self.frame = tk.Frame(width=600, height=400)
        self.frame.pack()
        self.frame.place(anchor='center', x=550, y=150)
        img = self.__load_img()
        self.label = tk.Label(self.frame, image = img)
        self.label.pack()
        
        self.mainloop()
    #play a sound
    def __play_sound(self, text):
        sound_wave = gTTS(text=text, lang='en') #create sound wave
        sound_wave.save('wave.mp3') #save sound wave

        mixer.init()
        mixer.music.load("wave.mp3")
        mixer.music.play()
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)
        mixer.quit()
        os.remove('wave.mp3')
    #load_img
    def __load_img(self):
        return ImageTk.PhotoImage(Image.open(self.img_path).resize((400, 300), Image.ANTIALIAS))
    
    #search a word in csv file
    def __search_word(self):
        word = self.word_to_search.get()
        if word != '':
            self.__change_data(word=word)
        else:
            messagebox.showerror('Error', 'Please enter a word')

    #change data in app
    def __change_data(self, index=None, word=None):
        self.df = pd.read_csv('words.csv')
        if word:
            index = self.df[self.df['word'] == word].index.values[0]

        self.word = self.df.loc[index]['word']
        self.example = self.df.loc[index]['example']
        self.meaning = self.df.loc[index]['meaning']

        self.word_label.config(text=f"Word: {self.word}")

        self.meaning_label.config(text=f"Meaning: {self.meaning}")
        self.example_label.config(text=f"Example: {self.example}")

        self.img_path = self.df.loc[index]['image']
        img = self.__load_img()
        self.label.config(image='')
        self.label.image = img
        self.label.config(image=img)
    
    #edit word
    def __edit_word(self):
        self.edit = Edit()
        self.index = self.edit.index[0]
        self.__change_data(index=self.index)
    #slide to next word
    def __next_word(self):
        if self.index < len(self.df)-1:
            self.index += 1
            self.__change_data(index=self.index)
    #slide to previous word
    def __prev_word(self):
        if self.index > 0:
            self.index -= 1
            self.__change_data(index=self.index)
    #add word to csv file
    def __add_word(self):
        self.add = Add()
        self.index = self.add.index
        self.__change_data(index=self.index)

    #create button
    def __create_btn(self, text, command, x, y, bg='white', fg='black', font=('Courier', 20), width=3, height=1):
        self.btn = tk.Button(self, text=text, command=command, bg=bg, fg=fg, font=font)
        self.btn.place(x=x, y=y)

        return self.btn
    #create label
    def __create_label(self, text, x, y, bg='black', fg='white', font=('Courier', 20)):
        self.label = tk.Label(self, text=text, bg=bg, fg=fg, font=font)
        self.label.place(x=x, y=y)

        return self.label
    
app = App()