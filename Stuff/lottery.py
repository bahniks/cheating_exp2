#! python3
from tkinter import *
from tkinter import ttk
from time import perf_counter, sleep

import random
import os

from common import ExperimentFrame, InstructionsFrame
from gui import GUI


################################################################################

#introText = "ted se budete ucastnit loterie"

instructions = """V této úloze budete házet kostkou, dokud vám nepadne liché číslo.
Jakmile padne liché číslo, úloha končí a vám zůstává vaše dosažená výhra.
Vaše počáteční výhra je {} Kč a tato výhra se zdvojnásobí pokaždě, když vám padne sudé číslo.
Maximálně můžete takto vyhrát {} Kč.
"""

winningText = "Vaše současná výhra je: {} Kč"

losingText = "Tímto úloha končí. Vyhráli jste: {} Kč"

class Lottery(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        #######################
        # adjustable parameters
        self.displayNum = self.createDots # self.createDots or self.createText
        self.fakeRolling = True # False for testing
        self.diesize = 240
        self.startingReward = 5
        self.maximumReward = 320
        #######################

        self.width = self.root.screenwidth
        self.height = self.root.screenheight

        self.file.write("Lottery\n")

        self.upperText = Text(self, height = 5, width = 80, relief = "flat", font = "helvetica 15",
                              wrap = "word")
        self.upperText.insert("1.0", instructions.format(self.startingReward, self.maximumReward))
        self.upperText["state"] = "disabled"
        self.die = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                          background = "white", width = self.diesize, height = self.diesize)
        self.bottomText = Text(self, height = 3, width = 80, relief = "flat", font = "helvetica 15",
                               wrap = "word")
        self.currentReward = self.startingReward
        self.bottomText.insert("1.0", winningText.format(self.currentReward))
        self.bottomText["state"] = "disabled"
        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Hodit kostkou", command = self.roll)
         
        self.upperText.grid(column = 1, row = 1)
        self.die.grid(column = 1, row = 3, pady = 40)
        self.bottomText.grid(column = 1, row = 4)
        self.next.grid(row = 5, column = 1)

        self["highlightbackground"] = "white"
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)
        self.rowconfigure(6, weight = 4)        


    def roll(self):
        self.next["state"] = "disabled"
        self.die.create_rectangle((5, 5, self.diesize - 5, self.diesize - 5),
                                  fill = "white", tag = "die", outline = "black", width = 5)
        # fake rolling
        if self.fakeRolling:
            for roll in range(random.randint(4,6)):         
                self.displayNum(self.diesize/2, self.diesize/2, random.randint(1, 6))
                self.update()
                sleep(0.2)
                self.die.delete("dots")
        self.currentRoll = random.randint(1, 6)
        self.displayNum(self.diesize/2, self.diesize/2, self.currentRoll)
        self.bottomText["state"] = "normal"
        self.bottomText.delete("1.0", "end")
        if self.currentRoll % 2 == 0:
            self.currentReward *= 2
            if self.currentReward < self.maximumReward:
                self.bottomText.insert("1.0", winningText.format(self.currentReward))
        if self.currentRoll % 2 == 1 or self.currentReward >= self.maximumReward:
            self.bottomText.insert("1.0", losingText.format(self.currentReward))
            self.next["text"] = "Pokračovat"
            self.next["command"] = self.nextFun
            self.root.texts["lottery"] = self.currentReward
        self.bottomText["state"] = "disabled"
        self.update()
        self.next["state"] = "!disabled"


    def createDots(self, x0, y0, num):
        positions = {"1": [(0,0)],
                     "2": [(-1,-1), (1,1)],
                     "3": [(-1,-1), (0,0), (1,1)],
                     "4": [(-1,-1), (-1,1), (1,-1), (1,1)],
                     "5": [(-1,-1), (-1,1), (0,0), (1,-1), (1,1)],
                     "6": [(-1,-1), (-1,1), (1,-1), (1,1), (-1,0), (1,0)]}
        for x, y in positions[str(num)]:
            d = self.diesize/4
            coords = [x0 + x*d + d/3, y0 - y*d + d/3,
                      x0 + x*d - d/3, y0 - y*d - d/3]
            self.die.create_oval(tuple(coords), fill = "black", tag = "dots")


    def createText(self, x0, y0, num):
        self.die.create_text(x0, y0, text = str(num), font = "helvetica 70", tag = "die")
        
                   
    def write(self):
        self.file.write("\t".join(map(str, self.id + str(self.currentReward))) + "\n")
        

#LotteryInstructions = (InstructionsFrame, {"text": introText, "height": 5})


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([#LotteryInstructions,
         Lottery
         ])
