#! python3
from tkinter import *
from tkinter import ttk
from time import perf_counter, sleep

import random
import os

from common import ExperimentFrame, InstructionsFrame, Measure
from gui import GUI




WIN = 35
CURRENCY = "Kč"



################################################################################
# TEXTS

continuetext = "Pokračovat"

debrieftext = """
As was described before, the dice rolling task had two versions:

Version BEFORE, in which predictions are stated before the roll of a die. Afterwards, you see the outcome of the roll and learn whether your prediction was correct or not and how much you earned.

Version AFTER, in which you state whether your prediction was correct or incorrect and how much you earned after the roll of a die is made and you see its result.

Please rate how much do you agree or disagree with each of the following characterization for each version of the task.
"""

debriefquest1 = "How much do you agree that the BEFORE version of the task ..."
debriefquest2 = "How much do you agree that the AFTER version of the task ..."
debriefscale1 = "completely disagree"
debriefscale2 = "disagree"
debriefscale3 = "agree"
debriefscale4 = "completely agree"

debriefdimensions = ["... required attention",
                     "... required logical thinking",
                     "... enabled cheating",
                     "... made overreporting correct predictions acceptable",
                     "... the die roll was randomly generated"]



################################################################################

       
class DebriefCheating(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.text = Text(self, height = 11, width = 90, relief = "flat", font = "helvetica 15", wrap = "word")
        self.text.insert("1.0", debrieftext)
        self.text["state"] = "disabled"
        self.text.grid(row = 1, column = 1)

        self.frame1 = OneFrame(self, debriefquest1)
        self.frame1.grid(row = 2, column = 1)

        self.frame2 = OneFrame(self, debriefquest2)
        self.frame2.grid(row = 3, column = 1)            

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = continuetext, command = self.nextFun,
                               state = "disabled")
        self.next.grid(row = 4, column = 1, sticky = N)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 2)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)

    def check(self):
        if self.frame1.check() and self.frame2.check():
            self.next["state"] = "!disabled"
            return True

    def write(self):
        if self.check():
            self.file.write("Perception cheating\n" + self.id + "\t")
            self.frame1.write()
            self.file.write("\t")
            self.frame2.write()
            self.file.write("\n")



class OneFrame(Canvas):
    def __init__(self, root, question):
        super().__init__(root, background = "white", highlightbackground = "white",
                         highlightcolor = "white")

        self.root = root
        self.file = self.root.file

        self.answers = [debriefscale1, debriefscale2, debriefscale3, debriefscale4]
        
        self.lab1 = ttk.Label(self, text = question, font = "helvetica 15", background = "white")
        self.lab1.grid(row = 2, column = 1, pady = 10)
        self.measures = []
        for count, word in enumerate(debriefdimensions):
            self.measures.append(Measure(self, word, self.answers, "", "", function = self.root.check,
                                         labelPosition = "none"))
            self.measures[count].grid(row = count + 3, column = 1, columnspan = 2, sticky = E)

    def check(self):
        for measure in self.measures:
            if not measure.answer.get():
                return False
        else:
            return True             

    def write(self):
        for num, measure in enumerate(self.measures):
            self.file.write(str(self.answers.index(measure.answer.get()) + 1))
            if num != len(self.measures) - 1:
                self.file.write("\t")
     






if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([DebriefCheating
         ])
