#! /usr/bin/env python3
# -*- coding: utf-8 -*

from tkinter import *
from functools import partial
import pymysql
import requests

# Personnal mods
from conf import *


class Menu_Graphic(Frame):
    """This class displays main menu"""

    def __init__(self, parent, user, passw):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH)
        self.parent = parent
        
        # defining default data
        self.user = user
        self.passw = passw
        # creating client data
        self.connection = pymysql.connect(host='localhost',
                                user=self.user, \
                                password=self.passw, \
                                charset='utf8', \
                                cursorclass=pymysql.cursors.DictCursor)
        
    def main_menu(self):
        # button that allows user to choose category
        self.button_cat = Button(self, text="Find a product",
        command=partial(self.choose_category, self.parent), 
        height=3, width=15)
        self.button_cat.grid(column=0,row=0,sticky=W+E+N+S)

        # button that allows user to choose favorites
        self.button_fav = Button(self, text="My favorites", command=self.quit,
        height=3,width=15)
        self.button_fav.grid(column=0,row=1,sticky=W+E+N+S)

        # Button that makes you rage quit the program
        self.button_quit = Button(self, text="Quit", command=self.quit,
        height=3,width=15)
        self.button_quit.grid(column=0,row=2,sticky=N)

        # canvas displaying open food fact logo
        self.canvas = Canvas(self, width=225, height=225)
        self.canvas.grid(row=0, column=2, columnspan=2, rowspan=2,
                       sticky=W+E+N+S, padx=5, pady=5)
        self.img = PhotoImage(file='ressources/openfoodfact.png')
        self.canvas.create_image(112, 112, image=self.img)

    # this function will remove some widgets and add others
    def choose_category(self, parent):
        """This function displays categories"""

        #removing older widgets
        self.button_cat.destroy()
        self.button_fav.destroy()
        self.button_quit.destroy()

        #creating new ones
        self.Label = Label(self, text="Please choose a category", height=3, width=25)
        self.Label.grid(column=0, row=0)




if __name__=="__main__":
    fenetre=Tk()
    app = Menu_Graphic(fenetre, USERNAME, PASSWORD)
    app.main_menu()
    app.mainloop()
    fenetre.quit()