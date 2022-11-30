import tkinter as tk
import pandas as pd

from tkinter.filedialog import askopenfile
from tkinter import messagebox

class Edit(tk.Tk):
    def __init__(self):
        super().__init__()
        self.img_path = None
        self.df = pd.read_csv('words.csv')
        self.index = None
        self.__create_app()
    def __create_app(self):
        #app settings
        self.title('Edit Word')
        self.geometry('390x200')
        self.configure(bg='white')
        self.attributes('-topmost', True)

        #app widgets
        self.edit_word = self.__create_label('Word to edit:', 0, 0, bg='white', fg='black')
        self.word_to_edit = self.__create_entry(215, 2)
        self.new_word = self.__create_label('New word:', 0, 30, bg='white', fg='black')
        self.edited_word = self.__create_entry(215, 30)
        self.new_example = self.__create_label('New example:', 0, 60, bg='white', fg='black')
        self.edited_example = self.__create_entry(215, 60)
        self.new_meaning = self.__create_label('New meaning:', 0, 90, bg='white', fg='black')
        self.edited_meaning = self.__create_entry(215, 90)
        self.upload_img = self.__create_label('Upload image:', 0, 120, bg='white', fg='black')
        self.upload_img_btn = self.__create_btn('Upload', self.__upload_img, 215, 120, bg='white', fg='black', font=('Courier', 8))

        self.edit_btn = self.__create_btn('Edit', self.__edit, 150, 150, bg='white', fg='black', font=('Courier', 15), width=15, height=2)
        self.mainloop()
    #edit function
    def __edit(self):
        self.word = self.word_to_edit.get()
        self.index = self.df[self.df.word == self.word].index
        self.new_word = self.edited_word.get()
        self.new_example = self.edited_example.get()
        self.new_meaning = self.edited_meaning.get()
    
        if self.word == '':
            messagebox.showerror('Error', 'Please enter a word to edit')
        elif self.new_word == '' and self.new_example == '' and self.new_meaning == '' and self.img_path == None:
            messagebox.showerror('Error', 'Please enter a new word, example, meaning or upload an image')
        else:
            if self.df[self.df.word == self.word].empty == True:
                messagebox.showerror('Error', 'Word not found')
            else:
                if self.new_word != '':
                    self.df.loc[self.df.word == self.word, 'word'] = self.new_word
                if self.new_example != '':
                    self.df.loc[self.df.word == self.word, 'example'] = self.new_example
                if self.new_meaning != '':
                    self.df.loc[self.df.word == self.word, 'meaning'] = self.new_meaning
                if self.img_path != None:
                    self.df.loc[self.df.word == self.word, 'image'] = self.img_path
                self.df.to_csv('words.csv', index=False)
                messagebox.showinfo('Success', 'Word edited successfully')
                
                self.destroy()
                self.quit()  
            
    #upload image func
    def __upload_img(self):
        self.img = askopenfile(mode='r', filetypes=[('Image Files', '*.jpg *.png')])
        if self.img is not None:
            self.img_path = self.img.name
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
    #create entry
    def __create_entry(self, x, y):
        self.entry = tk.Entry(self)
        self.entry.place(x=x, y=y)

        return self.entry