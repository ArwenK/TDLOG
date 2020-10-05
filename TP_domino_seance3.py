#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 15:20:36 2020

@author: Alice Krychowski
Je n'étais pas là le jour du TP (j'étais dans la file d'attente pour effectuer un test PCR)
Et je n'ai pas réussi à trouver un binome, donc j'ai fait le TP seule
(des élèves m'ont dit que ce n'était pas obligatoire d'etre à deux).
Je pense que j'y ai consacré environ 3h
"""

import random as rd
import numpy as np
import copy as cp


Displaying_list = [["     ", "     ", "*    ", "*    ", "*   *", "*   *", "* * *"],
                   ["     ", "  *  ", "     ", "  *  ", "     ", "  *  ", "     "],
                   ["     ", "     ", "    *", "    *", "*   *", "*   *", "* * *"]]
D_list = np.array(Displaying_list, dtype=str)
Delimiting_line = "     +-----|-----+\n"
Space = "     "
# Store the patterns (strings) used for the representation of a domino


MAX_HAND_SIZE = 7

class domino:
    """Represents a domino"""

    def __init__(self, x0, y0, index0):
        assert (x0 < 7), "x too big"
        assert (y0 < 7), "y too big"
        self.x = x0
        self.y = y0
        self.index = index0

    @property
    def get_x(self):
        """
        Returns the left part of the domino
        """
        return self.x
    
    def get_y(self):
        """
        Returns the right part of the domino
        """
        return self.y
    
    def __repr__(self):
        """
        Returns a string corresponding to the Python representation
        """
        return "Domino(" + str(self.x) + ", " + str(self.y) + ")"

    def __str__(self):
        """
        Return the string that would display the domino onto the screen
        """
        line0 = Space + "|" + D_list[0][self.x] + "|" + D_list[0][self.y] + "|\n"
        str_index = " (" + str(self.index) + ")"
        if self.index < 10:
            str_index += " "
        line1 = str_index + "|" + D_list[1][self.x] + "|" + D_list[1][self.y] + "|\n"
        line2 = Space + "|" + D_list[2][self.x] + "|" + D_list[2][self.y] + "|\n"
        string = Delimiting_line + line0 + line1 + line2 + Delimiting_line
        return string

    def __eq__(self, other):
        """Returns True if self and other are equal  """
        return (self.x == other.x and self.y == other.y) or (self.y == other.x and self.x == other.y)

    def __ne__(self, other):
        """Returns True if self and other are different"""
        return not self.__eq__(other)

#domi1 = domino(1, 2, 10)
#domi2 = domino(6, 2, 10)
#print(domi1.__ne__(domi2))

def display_list(ls):
    """
    Entry : a list ls of tuple. Each tuple represents a domino
    Display the dominoes
    return nothing
    """
    for index in range(len(ls)):
        domi = domino(ls[index][0], ls[index][1], index + 1)
        print(domi.__str__())
    return None

"---------------------------------------- Part 2 ------------------------------------------"

def create_pile():
    """ Create a pile for a game"""
    pile = []
    for i in range(7):
        for j in range(i, 7):
            pile.append((i, j))
    rd.shuffle(pile)
    return pile


def inpu():
    """
    Ask the player to enter the indexes of the dominoes he/she wants to pull out
    Return a list of index of dominoes the player wishes to pull out
    """
    s = input("Enter one string to select the dominoes you want to pull out : ")
    l1 = list(s)
    l2 = []
    for element in l1:
        if element != " ":
            l2.append(int(element))
    return l2


def possible_discard(dominoes, number):
    sumList = [dom.get_x() + dom.get_y() for dom in dominoes]
    if len(sumList) == 0:
        return number == 0
    else:
        case_1 = dominoes[1:],number-sumList[0]
        return possible_discard(case_1) or possible_discard(dominoes[1:],number)



class hand:
    """Represents a hand of dominoes"""

    def __init__(self, pile):
        assert (len(pile) >= MAX_HAND_SIZE), "pile too small"
        self.ls = []
        for i in range(MAX_HAND_SIZE):
            self.ls.append(pile.pop())
        self.size = MAX_HAND_SIZE
        
    def get_size(self):
        """
        Returns the numbers of dominoes in the hand
        """
        return self.size
        
    def pull_out(self, instruction):
        """
        Argument : an instruction
        Check if it is possible to execute this instruction.
        If it is, the function execute the instruction and return true
        (so the game will know that the instruction was correct and can go to the next step)
        If it isn't, return False
        """
        total = 0
        for index in instruction:
            total += self.ls[index-1][0] + self.ls[index-1][1]
        if total == 12:
            instruction.sort(reverse=True)
            for index in instruction:
                self.ls.pop(index-1)
            return True
        else:
            print("The total was incorrect : the sum must be 12 and now it is ", total)
            return False

    def update(self, pile):
        """
        Until the pile is empty, complete the hand of the player.
        Return the number of dominoes left in the hand
        """
        for i in range(MAX_HAND_SIZE - len(self.ls)):
            if len(pile) > 0:
                self.ls.append(pile.pop())
        self.size = len(self.ls)
        return self.size

    def display(self):
        """Display the hand of the player on the screen"""
        display_list(self.ls)
        return None
    
    def playable(self, number):
        """Tests if dominoes can be discarded so that their sum is equal to number"""
        return(possible_discard(self.ls, number))
    

class Solitaire:
    
    def __init__(self):
        self.pile = create_pile()
        self.hand_of_player = hand(self.pile)
    
    def is_game_won(self): 
        """Return True iff the game is over and the player won"""
        return (len(self.pile) == 0) and (self.hand_of_player.get_size() == 0)
    
    def is_game_lost(self, number): 
        """return True iff the game is over and the player lost"""
        return(self.hand_of_player.playable(number))
        

#def game():
#    """A solitary game of dominoes"""
#    print("Welcome to the game ! \n")
#    pile = create_pile()
#    victory = False
#    hand_of_player = hand(pile)
#    hand_of_player.display()
#    print("There is ", len(pile), " dominoes left in the pile")
#
#    while victory != True:
#
#        instruction = inpu()
#        correctness_of_instruction = hand_of_player.pull_out(instruction)
#        # If the instruction is correct, the dominoes have now been pulled out
#        # Else, the player will have to enter an other instruction
#        while correctness_of_instruction == False:
#            instruction = inpu()
#            correctness_of_instruction = hand_of_player.pull_out(instruction)
#
#        size_of_hand = hand_of_player.update(pile)
#        print("\nYour instruction was executed. Here is your new hand : \n")
#        hand_of_player.display()
#        print("There is ", len(pile), " dominoes left in the pile")
#        victory = (len(pile) == 0) and (size_of_hand == 0)
#    print("VICTORY !!!")

#if __name__ == "__main__":
#    game()
