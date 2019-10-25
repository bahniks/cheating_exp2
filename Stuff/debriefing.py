#! python3

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import time, localtime, strftime, sleep

import random
import os.path
import os

from common import ExperimentFrame, InstructionsFrame, read_all, Measure
from gui import GUI



##################################################################################################################
# TEXTS #
#########

q1 = "In this and the following part, we are interested in finding out your opinion about the experiment. Please write down your opinion in a few sentences."
q2 = "Do you have any comments about the course of the experiment? Were the instructions clear? Was the user interface easy to follow? Do you have any comments regarding the behavior of experimenters? Is there anything you would do differently?"
q3 = "In your opinion, what was the aim of the task where you had to predict whether odd or even number would be rolled on a die? Please state, why you chose in this task the way you did."
q4 = "In your opinion, what was the aim of the task, where you had the option to donate money to a charity? Please state, why you chose in this task the way you did."
q5 = "Do you think it would be immoral to overreport the number of correctly predicted die rolls if given the chance in the dice rolling task in order to earn more money from the experimenter? Please also provide the reason for your answer."

czech = "You can answer these questions in Czech if you prefer so."

##################################################################################################################



class Debriefing(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.file.write("Debriefing\n")

        if COUNTRY == "CZECHIA":
            self.label = Text(self, wrap = "word", font = "helvetica 13",
                              relief = "flat", height = 1, cursor = "arrow",
                              selectbackground = "white", selectforeground = "black")
            self.label.insert("1.0", czech, "center")
            self.label.tag_config("center", justify = "center")
            self.label.config(state = "disabled")
            self.label.grid(column = 1, row = 0)


        self.question1 = Question(self, q1, alines = 4)
        self.question2 = Question(self, q2, alines = 4, qlines = 3)
        self.question3 = Question(self, q3, alines = 4)
        self.question4 = Question(self, q4, alines = 4)
        self.question5 = Question(self, q5, alines = 4, qlines = 3)

        self.question1.grid(row = 1, column = 1, sticky = "w")
        self.question2.grid(row = 2, column = 1, sticky = "w")
        self.question3.grid(row = 3, column = 1, sticky = "w")
        self.question4.grid(row = 4, column = 1, sticky = "w")
        self.question5.grid(row = 5, column = 1, sticky = "w")
        
        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Continue", command = self.nextFun)
        self.next.grid(row = 6, column = 1)

        self.warning = ttk.Label(self, text = "Please answer all questions.",
                                 background = "white", font = "helvetica 15", foreground = "white")
        self.warning.grid(row = 7, column = 1)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)
        self.rowconfigure(6, weight = 1)
        self.rowconfigure(7, weight = 1)
        self.rowconfigure(8, weight = 2)

        
    def check(self):
        return self.question1.check() and self.question2.check() and \
               self.question3.check() and self.question4.check() and self.question5.check()

    def back(self):
        self.warning.config(foreground = "red")

    def write(self):
        self.file.write(self.id + "\t")
        self.question1.write(newline = False)
        self.file.write("\t")
        self.question2.write(newline = False)
        self.file.write("\t")
        self.question3.write(newline = False)
        self.file.write("\t")
        self.question4.write(newline = False)
        self.file.write("\t")
        self.question5.write()

       
class Question(Canvas):
    def __init__(self, root, text, width = 80, qlines = 2, alines = 5):
        super().__init__(root)
        self["background"] = "white"
        self["highlightbackground"] = "white"
        self["highlightcolor"] = "white"

        self.root = root

        self.answer = StringVar()

        self.label = Text(self, width = width, wrap = "word", font = "helvetica 15",
                          relief = "flat", height = qlines, cursor = "arrow",
                          selectbackground = "white", selectforeground = "black")
        self.label.insert("1.0", text)
        self.label.config(state = "disabled")
        self.label.grid(column = 0, row = 0)

        self.field = Text(self, width = int(width*1.2), wrap = "word", font = "helvetica 13",
                          height = alines, relief = "solid")
        self.field.grid(column = 0, row = 1, pady = 6)

        self.columnconfigure(0, weight = 1)


    def check(self):
        return self.field.get("1.0", "end").strip()

    def write(self, newline = True):
        self.root.file.write(self.field.get("1.0", "end").replace("\n", "  ").replace("\t", " "))
        if newline:
            self.root.file.write("\n")

    def disable(self):
        self.field.config(state = "disabled")


            

def main():
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Debriefing])


if __name__ == "__main__":
    main()

