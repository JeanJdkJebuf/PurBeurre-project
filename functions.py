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