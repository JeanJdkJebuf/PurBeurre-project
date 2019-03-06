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
            self.list_products.append(row)
        
        #function to creates 10 products
        self.creating_prod_button(self.parent,self.product_marker)
        #function that creates next and previous buttons
        self.button_next(self.parent)

    # this function creates Buttons of certain products (x to x+10)
    def creating_prod_button(self, parent, prod_mark):
        """this function creates Buttons from prod_mark
        to prod_mark+10 used for function choose_product"""

        # forced to do it here, because of next and previous buttons
        # creating products only, requirement for 
        # creating buttons naimed after them
        self.list_prod_name=[]
        for x in range(len(self.list_products)):
            self.list_prod_name.append(self.list_products[x][1])

        #marker for buttons rows
        t=0
        # loop creating product buttons
        for x in range(prod_mark, prod_mark+10):
            #converting product name and number into var
            var_number=self.list_products[x]
            #creating buttons
            self.list_prod_name[x]=Button(self, text=self.list_prod_name[x],\
            command=partial(self.showing_product, \
            self.parent, var_number), height=3, width=15)
            self.list_prod_name[x].grid(column=0, row=t, sticky=W+E+N+S)
            # increasing marker
            t += 1
    
    #this button once clicked will show 10 next results
    def button_next(self, parent):
        """This buttons will show 10 next or previous
        results if possible"""

        #testing if button next can be pressed
        def test_sup(number):
            if self.product_marker+number in range(len(self.list_products)):
                #removing previous widgets
                for x in range(self.product_marker, self.product_marker+10):
                    self.list_prod_name[x].destroy()
                #updating self.product_marker
                self.product_marker += number
                #creating new widgets
                self.creating_prod_button(self.parent,self.product_marker)

        self.but_next=Button(self, text="next", \
        command=partial(test_sup, +10), height=3, width=15)
        self.but_next.grid(column=2, row=11)

        self.but_prev=Button(self, text="previous", \
        command=partial(test_sup, -10), height=3, width=15)
        self.but_prev.grid(column=1, row=11)

    
    def showing_product(self, parent, prod_info):
        """this function will display a new window.
        This window will show current product, and
        a substitute"""

        fen=Toplevel(parent)
        fen.title("product features")
        # grab_set denies user to use main window while this 
        # window is opened
        fen.grab_set()

        lab1 = LabelFrame(fen, text="Current product", padx=20, pady=20)
        lab1.grid(ipadx=20, ipady=20)
        fen.rowconfigure(0, weight=1)
        fen.columnconfigure(0)

        # adding text
        for x in range(len(DISPLAY_INFO)):
            # adding informations
            lab=Label(lab1, text=DISPLAY_INFO[x],height=3, width=15)
            lab.grid(column=0,row=x, sticky=W)
            # adding product informations
            jeanjean=Label(lab1, text=prod_info[x+1], height=3, width=75)
            jeanjean.grid(column=1,row=x, sticky=E)



if __name__=="__main__":
    fenetre=Tk()
    fenetre.title("Smart food finder")
    app = Menu_Graphic(fenetre, USERNAME, PASSWORD)
    app.main_menu()
    app.mainloop()
    fenetre.quit()