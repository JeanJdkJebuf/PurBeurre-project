#!/usr/bin/python3
# -*- coding: utf-8 -*

# functions for PurBeurre-project


# function that replaces letters to numbers
# meant for nutrition_grade
def replace_let(letter):
    """This function replaces letters
    to numbers, to make it easier to
    research substitutes"""

    # list of possible letters
    let = ["a", "b", "c", "d", "e"]
    if letter in let:
        return let.index(letter)
    else:
        pass


# function made for user_interface.py
def cut_str(line, number, cut):
    """This function adds \n in str to allow
    tkinter to show informations correctly,
    line is the var, number is the number before
    you want to cut the line. If cut = 0,
    this function doesn't care about space"""
    ranged = (0, number)
    # string that will replace line
    t = 0
    replace_str = ""
    space_str = " "
    if cut == 0:
        for x in range(len(line)):
            if x % number in ranged and x:
                replace_str += line[x]+"\n"
            else:
                replace_str += line[x]
    else:
        for x in range(len(line)):
            if x % number in ranged and x:
                t = 1
            if t == 1 and line[x] == space_str:
                replace_str += line[x]+"\n"
                t = 0
            else:
                replace_str += line[x]
    return replace_str
