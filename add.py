import tkinter as tk
import pandas as pd

from tkinter.filedialog import askopenfile

class Add(tk.Tk):
    def __init__(self):
        super().__init__()
        self.img_path = None
        self.df = pd.read_csv('words.csv')
        self.__create_app()
    def __create_app(self):
        #app settings
        self.title('Add Word')
        self.geometry('390x160')
        self.configure(bg='white')
        self.attributes('-topmost', True)

        #app widgets
        self.new_word = self.__create_label('New word:', 0, 0, bg='white', fg='black')
        self.word_to_add = self.__create_entry(215, 2)
        self.new_example = self.__create_label('New example:', 0, 30, bg='white', fg='black')
        self.edited_example = self.__create_entry(215, 32)
        self.new_meaning = self.__create_label('New meaning:', 0, 60, bg='white', fg='black')
        self.edited_meaning = self.__create_entry(215, 62)
        self.upload_img = self.__create_label('Upload image:', 0, 90, bg='white', fg='black')
        self.upload_img_btn = self.__create_btn('Upload', self.__upload_img, 215, 90, bg='white', fg='black', font=('Courier', 8))

        self.edit_btn = self.__create_btn('Add', self.__add, 150, 120, bg='white', fg='black', font=('Courier', 15), width=15, height=2)
        self.mainloop()
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
    #upload image
    def __upload_img(self):
        self.img_path = askopenfile(mode='r', filetypes=[('Image Files', '*.*')])
    #add new word
    def __add(self):
        self.new_word = self.word_to_add.get()
        self.new_example = self.edited_example.get()
        self.new_meaning = self.edited_meaning.get()
        if self.img_path:
            self.new_img = self.img_path.name
        else:
            self.new_img = 'images/no_img.jpg'

        if self.new_word == '':
            tk.messagebox.showerror('Error', 'Please enter a word')
        else:
            self.df.loc[len(self.df)] = [self.new_word, self.new_example, self.new_meaning, self.new_img]
            self.df.to_csv('words.csv', index=False)
            tk.messagebox.showinfo('Success', 'Word edited successfully')
            self.index = len(self.df) - 1
            self.destroy()
            self.quit()
