#! /usr/bin/env python3
# -*- coding: utf-8 -*

from tkinter import *
from functools import partial
import pymysql
import requests
from functions import cut_str, callback

# Personnal mods
from conf import *
from dao import *
from text import *



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
        self.p = PanedWindow(self, orient=VERTICAL)
        self.p.pack(side=LEFT, expand=Y, fill=BOTH, pady=2, padx=2)
        # button that allows user to choose category
        self.button_cat = Button(self.p, text="Produits",
        command=self.choose_category, 
        height=3, width=15)
        self.button_cat.pack()

        # button that allows user to choose favorites
        self.button_fav = Button(self.p, text="Mes favoris", \
        command=self.show_favorites, height=3,width=15)
        self.button_fav.pack()

        # canvas displaying open food fact logo
        self.canvas = Canvas(self, width=225, height=225)
        self.canvas.pack()
        self.img = PhotoImage(file='ressources/openfoodfact.png')
        self.canvas.create_image(112, 112, image=self.img)

        # Label explaining what's happening
        self.lab1 = Label(self, text=explain_menu)
        self.lab1.pack()

        # Button that makes you quit the program
        self.button_quit = Button(self.p, text="Quitter", command=self.quit,
        height=3,width=15)
        self.button_quit.pack(side=BOTTOM)


    # this function will remove some widgets and add others
    def choose_category(self):
        """This function displays categories"""

        # removing older widgets
        self.p.destroy()
        self.button_cat.destroy()
        self.button_fav.destroy()
        self.button_quit.destroy()
        self.canvas.destroy()
        self.lab1.destroy()

        # getting Categories names in liste
        self.cur=self.connection.cursor()
        self.cur.execute("SELECT category_name FROM Categories;")
        self.liste=[]
        for row in self.cur:
            self.liste.append(''.join(row))
        
        # LabelFrame created to not mess up with layout
        self.l = LabelFrame(self, text="Categories")
        self.l.grid(column=0, row=0)
        # creating Categories Buttons
        col, ligne = 0, 0
        for func in range(len(self.liste)):
            if not func % 6 :
                col += 1
                ligne = 0

            self.liste[func]=Button(self.l, text=self.liste[func], command=partial(self.choose_product, func+1),
            height=3, width=15)
            self.liste[func].grid(column=col,row=ligne+1,sticky=W+E+N+S)
            ligne += 1

        # Paned window to display informations with a good layout
        self.p2 = PanedWindow(self, orient=VERTICAL)
        self.p2.grid(column=1, row=0, sticky=N+S+E+W)

        # canvas displaying open food fact logo
        self.canvas = Canvas(self.p2, width=110, height=110)
        self.canvas.grid(column=1, row=0, sticky=N+E)
        self.img = PhotoImage(file='ressources/open_mini.png')
        self.canvas.create_image(55, 55, image=self.img)

        # Explanation text
        self.expl = Label(self.p2, text= expl_cat)
        self.expl.grid(column=1, row=1)

        # Back to main menu
        self.button_quit_1=Button(self.p2, text="Menu principal", command=self.back_from_cat, \
        height=3, width=15)
        self.button_quit_1.grid(column=1, row=2, sticky=S+E)

    #back to main menu, from products
    def back_from_cat(self):
        while True:
            try:
                self.l.destroy()
                self.expl.destroy()
                for func in range(len(self.liste)):
                    self.liste[func].destroy()
                self.canvas.destroy()
                self.expl.destroy()
                self.button_quit_1.destroy()
                self.p2.destroy()
            finally:
                self.main_menu()
                break

    def choose_product(self, category_number):
        """This function displays products
        of category_number of Products in bd"""

        # Creating product_marker, 
        # for creating_prod_button function
        self.product_marker=0

        # removing older widgets
        # for performance issues
        # (could clean with only destroy p2 and l)
        for func in self.liste:
            func.destroy()
        self.l.destroy()
        self.expl.destroy()
        for func in range(len(self.liste)):
            self.liste[func].destroy()
        self.canvas.destroy()
        self.p2.destroy()
        self.button_quit_1.destroy()

        # saving products in a list
        self.cur=self.connection.cursor()
        self.cur.execute(PRODUCT_SEARCH.format(category_number))
        self.list_products=[]
        for row in self.cur:
            self.list_products.append(row)
        
        # LabelFrame that will include products
        self.lpf = LabelFrame(self, text="Produits")
        self.lpf.grid(column=0, row=1)

        #function to creates 10 products and display marks
        self.creating_prod_button(self.product_marker)
        #function that creates next and previous buttons
        self.button_next()

        # Paned window to display informations with a good layout
        self.p2 = PanedWindow(self, orient=VERTICAL)
        self.p2.grid(column=1,row =1, sticky=N+S+E+W)

        # canvas displaying open food fact logo
        self.canvas = Canvas(self.p2, width=110, height=110)
        self.canvas.grid(column=0, row=0, sticky=N+E)
        self.img = PhotoImage(file='ressources/open_mini.png')
        self.canvas.create_image(55, 55, image=self.img)

        # Explanation text
        self.expl = Label(self.p2, text= expl_prod)
        self.expl.grid(column=0, row=1)

        # Back to main menu
        self.button_quit_1=Button(self, text="Menu principal", command=self.back_to_menu, \
        height=3, width=15)
        self.button_quit_1.grid(column=1, row=2, sticky=S+E)

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
        y=0
        while True:
            if prod_mark+10 > len(self.list_products):
                # label that show user number of procuts
                self.lab_show=Label(self.lpf, text=show_num.format(prod_mark+1, \
                len(self.list_products)+1, len(self.list_products)+1), \
                padx=20, pady=20)
                self.lab_show.grid(column=1, row=0)
                for x in range(prod_mark, len(self.list_products)):
                    #converting product name into var
                    var_number=self.list_products[x]
                    # algorithm displaying informations on multiple columns
                    if not x % 5:
                        y+=1
                        t=1
                    #creating buttons
                    self.list_prod_name[x]=Button(self.lpf, text=cut_str(self.list_prod_name[x], 25, 1), \
                    command=partial(self.showing_product, \
                    self.parent, var_number), height=3, width=28)
                    self.list_prod_name[x].grid(column=y, row=t, sticky=W+E+N+S)
                    # increasing marker
                    t += 1
                break
            else:
                # label that show user number of procuts
                self.lab_show=Label(self.lpf, text=show_num.format(prod_mark+1, \
                prod_mark+11, len(self.list_products)+1), padx=20, pady=20)
                self.lab_show.grid(column=1, row=0)
                for x in range(prod_mark, prod_mark+10):
                    #converting product name into var
                    var_number=self.list_products[x]
                    # algorithm displaying informations on multiple columns
                    if not x % 5:
                        y+=1
                        t=1
                    #creating buttons
                    self.list_prod_name[x]=Button(self.lpf, text=cut_str(self.list_prod_name[x], 25, 1), \
                    command=partial(self.showing_product, \
                    self.parent, var_number), height=3, width=28)
                    self.list_prod_name[x].grid(column=y, row=t, sticky=W+E+N+S)
                    # increasing marker
                    t += 1
                break
    
    #this button once clicked will show 10 next results
    def button_next(self):
        """This buttons will show 10 next or previous
        results if possible"""

        #testing if button next can be pressed
        def test_sup(number):
            if self.product_marker+number in range(len(self.list_products)):
                #destroying self.lab_show
                self.lab_show.destroy()
                #removing previous widgets
                for x in range(self.product_marker, self.product_marker+10):
                    self.list_prod_name[x].destroy()
                #updating self.product_marker
                self.product_marker += number
                #creating new widgets
                self.creating_prod_button(self.product_marker)
        
        # creating a panedwindow to implemente buttons for a correct layout
        self.pan1 = PanedWindow(self, orient=HORIZONTAL)
        self.pan1.grid(column=0, row=2)

        self.but_next=Button(self.pan1, text="suivant", \
        command=partial(test_sup, +10), height=3, width=15)
        self.but_next.grid(column=1, row=0, sticky=W+E+N+S)

        self.but_prev=Button(self.pan1, text="précédent", \
        command=partial(test_sup, -10), height=3, width=15)
        self.but_prev.grid(column=0, row=0, sticky=W+E+N+S)

    # this button destroys all widgets and calls main_menu()
    def back_to_menu(self):

        while True:
            try:
                self.button_quit_1.destroy()
                self.lpf.destroy()
                self.but_next.destroy()
                self.but_prev.destroy()
                while True:
                    if self.product_marker+10>len(self.list_products):
                        for x in range(self.product_marker, len(self.list_products)):
                            self.list_prod_name[x].destroy()
                        break
                    else:
                        for x in range(self.product_marker, self.product_marker+10):
                            self.list_prod_name[x].destroy()
                        break
                self.lab_show.destroy()
                self.pan1.destroy()
                self.expl.destroy()
                self.canvas.destroy()
                self.p2.destroy()             
            finally:
                #calls main_menu
                self.main_menu()
                break
    
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
        lab1 = LabelFrame(fen, text="Description produit", padx=10, pady=10)
        lab1.grid(ipadx=10, ipady=10,column=0,row=0)

        # second frame, displaying substitute
        lab2 = LabelFrame(fen, text="substitut proposé", padx=10, pady=10)
        lab2.grid(ipadx=10, ipady=10,column=0,row=1)


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
                    # if no substitutes found
                    # rare error, will be fixed afterwards
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
            lab=Label(lab1, text=DISPLAY_INFO[x],height=5, width=15)
            lab.grid(column=0,row=x, sticky=W)

        Label(lab1, text=cut_str(prod_info[1], 70, 0), height=4, \
        width=75).grid(column=1, row=0, sticky=E)
        Label(lab1, text=cut_str(prod_info[2], 70, 0), height=4, \
        width=75).grid(column=1, row=1, sticky=E)
        link=Label(lab1, text=cut_str(prod_info[3], 70, 0), height=4, \
        width=75, fg="blue", cursor="hand2")
        link.grid(column=1, row=2, sticky=E)
        link.bind("<Button-1>", callback)
        Label(lab1, text=cut_str(prod_info[4], 70, 0), height=4, \
        width=75).grid(column=1, row=3, sticky=E)
        Label(lab1, text=cut_str(prod_info[5], 70, 0), height=4, \
        width=75).grid(column=1, row=4, sticky=E)
        
        # adding text in lab2 (substitute)
        for x in range(len(DISPLAY_INFO)):
            # adding informations
            lab=Label(lab2, text=DISPLAY_INFO[x],height=3, width=15)
            lab.grid(column=0,row=x, sticky=W)
        while True:
            try: 
                Label(lab2, text=cut_str(substitute[0][0], 70, 0), height=4, \
                width=75).grid(column=1, row=0, sticky=E)
                Label(lab2, text=cut_str(substitute[0][1], 70, 0), height=4, \
                width=75).grid(column=1, row=1, sticky=E)
                link=Label(lab2, text=cut_str(substitute[0][2], 70, 0), height=4, \
                width=75, fg="blue", cursor="hand2")
                link.grid(column=1, row=2, sticky=E)
                link.bind("<Button-1>", callback)
                Label(lab2, text=cut_str(substitute[0][3], 70, 0), height=4, \
                width=75).grid(column=1, row=3, sticky=E)
                Label(lab2, text=cut_str(substitute[0][4], 70, 0), height=4, \
                width=75).grid(column=1, row=4, sticky=E)
            except:
                # if there's no substitute, print that message
                if not substitute:
                    error_msg=Label(lab2, text="No substitute found",
                    height=3, width=75)
                    error_msg.grid(column=1,row=0,sticky=E)
            finally:
                button_substitute=Button(lab2, text="Add to favorites", \
                command=partial(add_to_favorites, substitute[0][5]),
                height=1, width=15)
                button_substitute.grid(column=1, row=5)
                break

    def show_favorites(self):
        """this function shows Favorites"""

        #destroying main menu widgets
        self.p.destroy()
        self.button_cat.destroy()
        self.button_fav.destroy()
        self.button_quit.destroy()
        self.canvas.destroy()
        self.lab1.destroy()

        self.listefav=[]
        cur=self.connection.cursor()
        cur.execute(GETTING_FAV_DATA)
        for row in cur:
            self.listefav.append(row)

        # adding list of names for "back to menu"
        # if i don't do it, we can't go back to menu
        self.name_fav=[]
        for x in self.listefav:
            self.name_fav.append(x[0])

        #adding a LabelFrame to display list of favorites in it
        self.lfpf = LabelFrame(self, text="Favoris")
        self.lfpf.grid(column=0, row=0)
        # adding buttons
        # adding a marker to display buttons over columns (10by column)
        z, y, mod_10 = 0, 0, 10 # z is for columns, x for rows
        for x in range(len(self.listefav)):
            if x%mod_10 == mod_10 or not x%mod_10:
                z+=1
                y=0
            self.name_fav[x]=Button(self.lfpf, text= cut_str(self.listefav[x][0],25,1), \
            command=partial(self.showing_fav, \
            self.parent, self.listefav[x]), height=2, \
            width=28)
            self.name_fav[x].grid(column=z, row=y)
            y+=1
        # Paned window to display informations with a good layout
        self.p22 = PanedWindow(self, orient=VERTICAL)
        self.p22.grid(column=1, row=0, sticky=N+S+E+W)

        # canvas displaying open food fact logo
        self.canvas2 = Canvas(self.p22, width=110, height=110)
        self.canvas2.grid(column=1, row=0, sticky=N+E)
        self.img = PhotoImage(file='ressources/open_mini.png')
        self.canvas2.create_image(55, 55, image=self.img)

        # Explanation text
        self.expl2 = Label(self.p22, text= expl_fav)
        self.expl2.grid(column=1, row=1)

        self.button_quit_2=Button(self.p22, text="Menu principal", command=self.back_from_fav, \
        height=3, width=15)
        self.button_quit_2.grid(column=1, row=2, sticky=S+E)
    
    # back to main menu (show_favorites func)
    def back_from_fav(self):
        
        while True:
            try:
                for x in range(len(self.listefav)):
                            self.name_fav[x].destroy()
                self.lfpf.destroy()
                self.p22.destroy()
                self.canvas2.destroy()
                self.expl2.destroy()
                self.button_quit_2.destroy()
            finally:
                #calls main_menu
                    self.main_menu()
                    break
                    

    def showing_fav(self, parent, prod_info):
        """Displaying new window, showing substitute"""

        fen=Toplevel(parent)
        fen.title("product features")
        # grab_set denies user to use main window while this 
        # window is opened
        fen.grab_set()

        # first frame, displaying current product
        lab1 = LabelFrame(fen, text="Current product")
        lab1.grid(column=0,row=0)

        # displaying product informations
        for line in range(len(DISPLAY_INFO)):
            Label(lab1, text=DISPLAY_INFO[line], height=3, \
            width=35).grid(column=0, row=line, sticky=W)

        Label(lab1, text=cut_str(prod_info[0], 70, 0), height=4, \
        width=75).grid(column=1, row=0, sticky=E)
        Label(lab1, text=cut_str(prod_info[1], 70, 0), height=4, \
        width=75).grid(column=1, row=1, sticky=E)
        link=Label(lab1, text=cut_str(prod_info[2], 70, 0), height=4, \
        width=75, fg="blue", cursor="hand2")
        link.grid(column=1, row=2, sticky=E)
        link.bind("<Button-1>", callback)
        Label(lab1, text=cut_str(prod_info[3], 70, 0), height=4, \
        width=75).grid(column=1, row=3, sticky=E)
        Label(lab1, text=cut_str(prod_info[4], 70, 0), height=4, \
        width=75).grid(column=1, row=4, sticky=E)




if __name__ == "__main__":
    None
