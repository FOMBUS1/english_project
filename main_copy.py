import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from PIL import ImageTk, Image


#App for learning english words
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.df = pd.read_csv('words.csv')
        self.__load_words(index=self.index)
        self.__create_app()
    #load_data
    def __load_words(self, index=1):
        self.word = self.df['word'][index]
        self.example = self.df['example'][index]
        self.meaning = self.df['meaning'][index]
        self.img_path = self.df['photo'][index]
    #create app
    def __create_app(self, width=1100, height=800):
        self.geometry(f'{width}x{height}')
        self.title('English Words')
        self.configure(bg='black')
        self.resizable(False, False)

        self.next_btn = self.__create_btn('->', self.__next_word, width-100, height-100)
        self.prev_btn = self.__create_btn('<-', self.__prev_word, 50, height-100)
        self.add_word_btn = self.__create_btn('Add Word', self.__add_word, width//2-300, height-100)
        self.edit_word_btn = self.__create_btn('Edit Word', self.__edit_word, width//2+100, height-100)
        self.search_btn = self.__create_btn('search', self.__search_word, width-120, 20, font=('Arial', 8))

        self.word_label = self.__create_label(f'Word: {self.word}', 50, height-400)
        self.example_label = self.__create_label(f'Example: {self.example}', 50, height-300)
        self.meaning_label = self.__create_label(f'Meaning: {self.meaning}', 50, height-200)

        self.word_to_search = self.search_input = tk.Entry(self)
        self.word_to_search.place(x=width-300, y=23)


        self.frame = tk.Frame(width=600, height=400)
        self.frame.pack()
        self.frame.place(anchor='center', x=550, y=150)
        img = self.__load_img()
        self.label = tk.Label(self.frame, image = img)
        self.label.pack()

        self.mainloop()
    #load_img
    def __load_img(self):
        return ImageTk.PhotoImage(Image.open(self.img_path).resize((400, 300), Image.ANTIALIAS))
    #search a word in csv file
    def __search_word(self):
        word = self.word_to_search.get()
        self.__change_data(word=word)

    #change data in app
    def __change_data(self, index=None, word=None):
        if word:
            index = self.df[self.df['word'] == word].index.values[0]

        self.word = self.df.loc[index]['word']
        self.word_label.config(text=f"Word: {self.word}")

        self.meaning_label.config(text=f"Meaning: {self.df.loc[index]['meaning']}")
        self.example_label.config(text=f"Example: {self.df.loc[index]['example']}")

        self.img_path = self.df.loc[index]['photo']
        img = self.__load_img()
        self.label.config(image='')
        self.label.image = img
        self.label.config(image=img)
    
    #edit word
    def __edit_word(self):
        pass
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
        pass
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