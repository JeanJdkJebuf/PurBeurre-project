#! /usr/bin/env python3
# -*- coding: utf-8 -*

from tkinter import *
from functools import partial
import pymysql
import requests

# Personnal mods
from conf import *
from functions import cut_str


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
        command=self.choose_category, 
        height=3, width=15)
        self.button_cat.grid(column=0,row=0,sticky=W+E+N+S)

        # button that allows user to choose favorites
        self.button_fav = Button(self, text="My favorites", \
        command=self.show_favorites, height=3,width=15)
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
    def choose_category(self):
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
            self.liste[func]=Button(self, text=self.liste[func], command=partial(self.choose_product, func+1),
            height=3, width=15)
            self.liste[func].grid(column=0,row=func+1,sticky=W+E+N+S)

    # this function displays products by page
    def choose_product(self, category_number):
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
        self.creating_prod_button(self.product_marker)
        #function that creates next and previous buttons
        self.button_next()

        # Button that brings back to main menu
        self.button_quit=Button(self, text="Main menu", \
        command=self.back_to_menu, height=3, width=10)
        self.button_quit.grid(column=0,row=11, sticky=W+E+N+S)

    # this function creates Buttons of certain products (x to x+10)
    def creating_prod_button(self, prod_mark):
        """this function creates Buttons from prod_mark
        to prod_mark+10 used for function choose_product"""

        # forced to do it here, because of next and previous buttons
        # creating products only, requirement for 
        # creating buttons naimed after them
        self.list_prod_name=[]
        for x in range(len(self.list_products)):
            self.list_prod_name.append(self.list_products[x][1])

        #marker for buttons rows
        t=1
        # loop creating product buttons
        for x in range(prod_mark, prod_mark+10):
            #converting product name and number into var
            var_number=self.list_products[x]
            #creating buttons
            self.list_prod_name[x]=Button(self, text=cut_str(self.list_prod_name[x], 25, 1), \
            command=partial(self.showing_product, \
            self.parent, var_number), height=3, width=15)
            self.list_prod_name[x].grid(column=0, row=t, sticky=W+E+N+S)
            # increasing marker
            t += 1
    
    #this button once clicked will show 10 next results
    def button_next(self):
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
                self.creating_prod_button(self.product_marker)

        self.but_next=Button(self, text="next", \
        command=partial(test_sup, +10), height=3, width=15)
        self.but_next.grid(column=2, row=11)

        self.but_prev=Button(self, text="previous", \
        command=partial(test_sup, -10), height=3, width=15)
        self.but_prev.grid(column=1, row=11)

    # this button destroys all widgets and calls main_menu()
    def back_to_menu(self):
        self.Label2.destroy()
        self.but_next.destroy()
        self.but_prev.destroy()
        for x in range(self.product_marker, self.product_marker+10):
            self.list_prod_name[x].destroy()
        self.button_quit.destroy()
        #calls main_menu
        self.main_menu()
    
    def showing_product(self, parent, prod_info):
        """this function will display a new window.
        This window will show current product, and
        a substitute"""

        fen=Toplevel(parent)
        fen.title("product features")
        # grab_set denies user to use main window while this 
        # window is opened
        fen.grab_set()

        # first frame, displaying current product
        lab1 = LabelFrame(fen, text="Current product", padx=10, pady=10)
        lab1.grid(ipadx=10, ipady=10,column=0,row=0)

        # second frame, displaying substitute
        lab2 = LabelFrame(fen, text="substitute", padx=10, pady=10)
        lab2.grid(ipadx=10, ipady=10,column=1,row=0)


        # Checking a substitute to current product
        cur=self.connection.cursor()
        # website category hierarchy
        cat_hierarchy=prod_info[6].split(",")
        #list for substitute
        substitute=[]
        # loop getting on bd a substitute
        for low_cat in range(len(cat_hierarchy)):
            for rech in range(prod_info[7]+1):
                try:
                    cur.execute(REQUEST_SUBSTITUTE.format(prod_info[0], \
                    rech, cat_hierarchy[-low_cat-1]))
                    for row in cur:
                        substitute.append(row)
                except:
                    pass
                finally:
                    break
        # test numbers of substitute this algorithm finds            
        #print(len(substitute))

        #function that adds a product to favorites
        def add_to_favorites(id_prod):
            """This function will add products to favorites"""
            cur=self.connection.cursor()
            cur.execute(INSERT_FAVORITE.format(id_prod))
            self.connection.commit()
            #print(INSERT_FAVORITE.format(id_prod))
        
        # adding text in lab1 (current product)
        for x in range(len(DISPLAY_INFO)):
            # adding informations
            lab=Label(lab1, text=DISPLAY_INFO[x],height=3, width=15)
            lab.grid(column=0,row=x, sticky=W)
            # adding product informations
            jeanjean=Label(lab1, text=cut_str(prod_info[x+1],70,0), height=3, width=75)
            jeanjean.grid(column=1,row=x, sticky=E)
        
        # adding text in lab2 (substitute)
        for x in range(len(DISPLAY_INFO)):
            # adding informations
            lab=Label(lab2, text=DISPLAY_INFO[x],height=3, width=15)
            lab.grid(column=0,row=x, sticky=W)
            # adding product informations
            try:
                jeanjean=Label(lab2, text=cut_str(substitute[0][x],70,0), height=3, width=75)
                jeanjean.grid(column=1,row=x, sticky=E)
            except:
                # if there's no substitute, print that message
                if not substitute:
                    error_msg=Label(lab2, text="No substitute found",
                    height=3, width=75)
                    error_msg.grid(column=1,row=x,sticky=E)
            finally:
                pass
        button_substitute=Button(lab2, text="Add to favorites", \
            command=partial(add_to_favorites, substitute[0][5]),
        height=1, width=15)
        button_substitute.grid(column=1, row=5)

    def show_favorites(self):
        """this function shows Favorites"""

        #destroying main menu widgets
        self.button_cat.destroy()
        self.button_fav.destroy()
        self.button_quit.destroy()
        self.canvas.destroy()

        listefav=[]
        cur=self.connection.cursor()
        cur.execute(GETTING_FAV_DATA)
        for row in cur:
            listefav.append(row)

        # adding buttons
        # adding a marker to display buttons over columns (10by column)
        z, y, mod_10 = 0, 0, 10 # z is for columns, x for rows
        for x in range(len(listefav)):
            if x%mod_10 == mod_10 or not x%mod_10:
                z+=1
                y=0
            Button(self, text= cut_str(listefav[x][0],25,1), command=partial(self.showing_fav, \
            self.parent, listefav[x]), height=3, \
            width=35).grid(column=z, row=y)
            y+=1
    
    def showing_fav(self, parent, prod_info):
        """Displaying new window, showing substitute"""

        fen=Toplevel(parent)
        fen.title("product features")
        # grab_set denies user to use main window while this 
        # window is opened
        fen.grab_set()

        # first frame, displaying current product
        lab1 = LabelFrame(fen, text="Current product", padx=10, pady=10)
        lab1.grid(ipadx=10, ipady=10,column=0,row=0)

        # displaying product informations
        for line in range(len(DISPLAY_INFO)):
            Label(lab1, text=DISPLAY_INFO[line], height=3, \
            width=35).grid(column=0, row=line, sticky=W)

            Label(lab1, text=cut_str(prod_info[line],70,0), height=3, \
            width=155).grid(column=1, row=line, sticky=E)



if __name__=="__main__":
    None