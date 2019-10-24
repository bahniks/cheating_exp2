#! python3
from tkinter import *
from tkinter import ttk

import os

from common import ExperimentFrame, InstructionsFrame
from gui import GUI



hexacointro = """
\n\n\n
V následující části bude uvedena řada výroků.

Přečtěte si, prosím, postupně každý výrok a vždy se rozhodněte, jak moc s ním souhlasíte nebo nesouhlasíte.
"""


HexacoInstructions = (InstructionsFrame, {"text": hexacointro})


class Hexaco(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.perpage = 10

        self.file.write("Hexaco\n")

        self.questions = []
        with open(os.path.join("Stuff", "hexaco.txt")) as f:
            for line in f:
                self.questions.append(line.strip())

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun,
                               state = "disabled")
        self.next.grid(row = self.perpage*2 + 2, column = 1)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(self.perpage*2 + 2, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)

        self.mnumber = 0
        
        self.createQuestions()


    def createQuestions(self):
        self.measures = []
        for i in range(self.perpage):
            m = Measure(self, self.questions[self.mnumber], shortText = str(self.mnumber + 1))
            m.grid(column = 0, columnspan = 3, row = i*2 + 1)
            self.rowconfigure(i*2 + 2, weight = 1)
            self.mnumber += 1
            self.measures.append(m)


    def nextFun(self):
        for measure in self.measures:
            measure.write()
            measure.grid_forget()
        if self.mnumber == len(self.questions):
            self.file.write("\n")
            self.destroy()
            self.root.nextFrame()
        else:
            self.next["state"] = "disabled"
            self.createQuestions()


    def check(self):
        for m in self.measures:
            if not m.answer.get():
                return
        else:
            self.next["state"] = "!disabled"



class Measure(Canvas):
    def __init__(self, root, text, shortText = ""):
        super().__init__(root)

        self.root = root
        self.text = shortText
        self.answer = StringVar()
        self["background"] = "white"
        self["highlightbackground"] = "white"
        self["highlightcolor"] = "white"

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 13")

        self.question = ttk.Label(self, text = text, background = "white",
                                  anchor = "center", font = "helvetica 14")
        self.question.grid(column = 0, row = 0, columnspan = 7, sticky = S)

        self.left = ttk.Label(self, text = "zcela nesouhlasím", background = "white",
                              font = "helvetica 13")
        self.right = ttk.Label(self, text = "zcela souhlasím", background = "white",
                               font = "helvetica 13")
        self.left.grid(column = 0, row = 1, sticky = E, padx = 5)
        self.right.grid(column = 6, row = 1, sticky = W, padx = 5)           

        for value in range(1, 6):
            ttk.Radiobutton(self, text = str(value), value = value, variable = self.answer,
                            command = self.check).grid(row = 1, column = value, padx = 4)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(6, weight = 1)
        self.rowconfigure(0, weight = 1)


    def write(self):
        ans = "{}\t{}\n".format(self.text, self.answer.get())
        self.root.file.write(self.root.id + "\t" + ans)


    def check(self):
        self.root.check()




if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([HexacoInstructions,
         Hexaco])
