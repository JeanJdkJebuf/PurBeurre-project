#! /usr/bin/env python3
# -*- coding: utf-8 -*

###########################################################
# This file will launch the program.
# DO NOT LAUNCH UNTIL YOU PROPERLY ENTERED YOUR
# USERNAME AND PASSWORD IN conf.py
###########################################################

###########################################################
# This programm will not launch if you didn't install
# Pymysql, tkinter or if you don't have a local
#                  mysql server
###########################################################

###########################################################
# For more informations, please read README.md
###########################################################

###########################################################
# This project is open source, feel free to share it,
# modify it, use it as you like. Enjoy !
###########################################################
# importing tkinter
from tkinter import *

# Personnal mods
from conf import *
from user_interface import *

if __name__ == "__main__":
    fenetre = Tk()
    fenetre.title("Smart food finder")
    app = Menu_Graphic(fenetre, USERNAME, PASSWORD)
    try:
        app.main_menu()
        app.mainloop()
    finally:
        app.connection.close()
        fenetre.quit()
