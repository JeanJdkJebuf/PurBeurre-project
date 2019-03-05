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
                                db='comparatif_alimentaire', \
                                password=self.passw, \
                                charset='utf8')
        
    def main_menu(self):
        # button that allows user to choose category
        self.button_cat = Button(self, text="Products",
        command=partial(self.choose_category, self.parent), 
        height=3, width=15)
        self.button_cat.grid(column=0,row=0,sticky=W+E+N+S)

        # button that allows user to choose favorites
        self.button_fav = Button(self, text="My favorites", command=self.quit,
        height=3,width=15)
        self.button_fav.grid(column=0,row=1,sticky=W+E+N+S)

        # Button that makes you quit the program
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

        # removing older widgets
        self.button_cat.destroy()
        self.button_fav.destroy()
        self.button_quit.destroy()
        self.canvas.destroy()

        # creating new ones
        self.Label = Label(self, text="Please choose a category", height=3, width=25)
        self.Label.grid(column=0, row=0)

        # getting Categories names in liste
        self.cur=self.connection.cursor()
        self.cur.execute("SELECT category_name FROM Categories;")
        self.liste=[]
        for row in self.cur:
            self.liste.append(''.join(row))

        # creating Categories Buttons
        for func in range(len(self.liste)):
            self.liste[func]=Button(self, text=self.liste[func], command=partial(self.choose_product, self.parent, func+1),
            height=3, width=15)
            self.liste[func].grid(column=0,row=func+1,sticky=W+E+N+S)

    # this function displays products by page
    def choose_product(self, parent, category_number):
        """This function displays products
        of category_number of Products in bd"""

        # Creating product_marker, 
        # for creating_prod_button function
        self.product_marker=0

        #removing older widgets
        self.Label.destroy()
        for func in self.liste:
            func.destroy()

        # widget displaying title
        self.Label2 = Label(self, text="Please choose a product", height=3,
        width=35)
        self.Label2.grid(column=0, row=0)

        # saving products in a list
        self.cur=self.connection.cursor()
        self.cur.execute(PRODUCT_SEARCH.format(category_number))
        self.list_products=[]
        for row in self.cur:
            self.list_products.append(''.join(row))
        print(self.list_products[0])

        self.creating_prod_button(self.parent,self.product_marker)

    # this function creates Buttons of certain products (x to x+10)
    def creating_prod_button(self, parent, prod_mark):
        """this function creates Buttons from prod_mark
        to prod_mark+10 used for function choose_product"""

        # loop creating product buttons
        for x in range(prod_mark, prod_mark+10):
            self.list_products[x]=Button(self, \
            text=self.list_products[x], command=self.quit, \
            height=3, width=15)
            self.list_products[x].grid(column=0, row=x+1, sticky=W+E+N+S)
        

if __name__=="__main__":
    fenetre=Tk()
    app = Menu_Graphic(fenetre, USERNAME, PASSWORD)
    app.main_menu()
    app.mainloop()
    fenetre.quit()