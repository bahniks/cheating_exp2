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

instructions = """V této úloze můžete vyhrát peníze.
Můžete se rozhodnout, že hodíte kostkou.
Vaše počáteční výhra je {} Kč a tato výhra se zdvojnásobí pokaždě, když vám padne sudé číslo.
Pokud padne liché číslo, úloha končí a výhru ztrácíte.
Maximálně můžete takto vyhrát {} Kč.
Pokud zmáčknete tlačítko 'Ukončit házení', úlohu ukončíte a odnesete si dosaženou výhru.
"""

winningText = "Vaše současná výhra je: {} Kč"
losingText = "Tímto úloha končí. Výhru jste ztratili."
maximumText = "Více již vyhrát nemůžete. Tímto úloha končí. Vyhráli jste: {} Kč"

class Lottery(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        #######################
        # adjustable parameters
        self.displayNum = self.createDots # self.createDots or self.createText
        self.fakeRolling = True # False for testing
        self.diesize = 240
        self.startingReward = 5
        self.maximumReward = 1280
        #######################

        self.width = self.root.screenwidth
        self.height = self.root.screenheight

        self.file.write("Lottery\n")

        self.upperText = Text(self, height = 7, width = 80, relief = "flat", font = "helvetica 18",
                              wrap = "word")
        self.upperText.insert("1.0", instructions.format(self.startingReward, self.maximumReward))
        self.upperText["state"] = "disabled"
        self.die = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                          background = "white", width = self.diesize, height = self.diesize)
        self.bottomText = Text(self, height = 3, width = 80, relief = "flat", font = "helvetica 18",
                               wrap = "word")
        self.currentReward = self.startingReward
        self.bottomText.insert("1.0", winningText.format(self.currentReward))
        self.bottomText["state"] = "disabled"
        ttk.Style().configure("TButton", font = "helvetica 18")
        self.nextRoll = ttk.Button(self, text = "Hodit kostkou", command = self.roll, width = 14)
        self.endRolls = ttk.Button(self, text = "Ukončit házení", command = self.end, width = 14)
         
        self.upperText.grid(column = 1, row = 1, columnspan = 2)
        self.die.grid(column = 1, row = 3, pady = 40, columnspan = 2)
        self.bottomText.grid(column = 1, row = 4, columnspan = 2)
        self.nextRoll.grid(row = 5, column = 1, sticky = E, padx = 50)
        self.endRolls.grid(row = 5, column = 2, sticky = W, padx = 50)

        self["highlightbackground"] = "white"
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)
        self.rowconfigure(6, weight = 4)        


    def roll(self):
        self.nextRoll["state"] = "disabled"
        self.endRolls["state"] = "disabled"
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
        if self.currentRoll % 2 == 1:
            self.bottomText.insert("1.0", losingText)
        elif self.currentReward >= self.maximumReward:
            self.bottomText.insert("1.0", maximumText.format(self.maximumReward))
        else:
            self.nextRoll["state"] = "!disabled"
        self.bottomText["state"] = "disabled"
        self.update()        
        self.endRolls["state"] = "!disabled"


    def end(self):
        self.root.texts["lottery"] = self.currentReward
        self.nextFun()


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
        


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Lottery
         ])
