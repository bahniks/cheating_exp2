#! python3
from tkinter import *
from tkinter import ttk
from collections import deque
from time import perf_counter, sleep

import random
import os

from common import ExperimentFrame, InstructionsFrame
from gui import GUI


items = [["car", "průměrná cena auta", "100 000 Kč", "900 000 Kč", "značky auta", "průměrná cena auta"],
         ["temperature", "průměrná teplota v Praze", "8°C", "28°C", "měsíce v roce", "průměrná teplota v měsíci"]
         ]

random.shuffle(items)


class Comparison(ExperimentFrame):
    def __init__(self, root, state = "first"):
        super().__init__(root)

        self.state = state

        if state == "first":
            self.file.write("Anchoring 1\n")
        else:
            self.file.write("Anchoring 2\n")

        self.answerVar = StringVar()

        self.question = "Je {} menší nebo větší než {}?"
        if state == "first":
            self.entryInstruction = "Uveďte do pole níže příklad {}."
        else:
            self.entryInstruction = "Jaká je {}?"
        self.text = Text(self, font = "helvetica 20", relief = "flat", background = "white",
                         width = 80, height = 1, pady = 7, wrap = "word")
        self.text.grid(row = 3, column = 1, columnspan = 2, sticky = S)
        self.text.tag_configure("center", justify = "center")

        ttk.Style().configure("TButton", font = "helvetica 18")

        if state == "second":
            self.warning = ttk.Label(self, text = "Odpověď musí být číslo!\n(pro desetinná místa použijte tečku)", font = "helvetica 20",
                                     background = "white", foreground = "white", justify = "center", state = "disabled")
            self.warning.grid(row = 6, column = 1, columnspan = 2)
        
        self.lower = ttk.Button(self, text = "Menší", command = self.lowerResponse)
        self.higher = ttk.Button(self, text = "Větší", command = self.higherResponse)
        self.nextButton = ttk.Button(self, text = "Pokračovat", command = self.proceed)

        self.blank = Canvas(self, height = 50, width = 1, background = "white",
                            highlightbackground = "white")
        self.blank.grid(row = 5, column = 0)

        self.columnconfigure(0, weight = 4)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 4)
        
        self.rowconfigure(0, weight = 7)
        self.rowconfigure(1, weight = 4)
        self.rowconfigure(3, weight = 5)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 2)
        self.rowconfigure(6, weight = 10)

        self.number = 0

        self.displayQuestion()
        

    def lowerResponse(self):
        self.response("lower")

    def higherResponse(self):
        self.response("higher")        


    def displayQuestion(self):
        if self.state == "first":
            randomValence = random.randint(2,3)
            self.anchor = items[self.number][randomValence]
            self.valence = "low" if randomValence == 2 else "high"
        self.text["state"] = "normal"
        if self.state == "first":
            self.text.insert("end", self.question.format(items[self.number][1], self.anchor), "center")
        else:
            self.text.insert("end", self.question.format(items[self.number][5] + " " + self.root.texts[items[self.number][0]],
                                                         items[self.number][1]), "center")
                                                         
        self.text["state"] = "disabled"

        self.lower.grid(row = 5, column = 1, sticky = E, padx = 20)
        self.higher.grid(row = 5, column = 2, sticky = W, padx = 20)


    def displayEntry(self):
        # pridat jednotky
        self.answer = ttk.Entry(self, textvariable = self.answerVar, font = "helvetica 20", width = 20)
        self.answer.grid(row = 4, column = 1, columnspan = 2, pady = 10)
        self.answer.bind("<KeyRelease>", self.checkEntry)
        self.nextButton.grid(row = 5, column = 1, columnspan = 2)
        self.nextButton["state"] = "disabled"
        self.text["state"] = "normal"
        index = 4 if self.state == "first" else 1
        self.text.insert("end", self.entryInstruction.format(items[self.number][index]), "center")
        self.text["state"] = "disabled"


    def checkEntry(self, e):           
        if self.answerVar.get():
            self.nextButton["state"] = "!disabled"
        else:
            self.nextButton["state"] = "disabled"
        

    def response(self, answer):
        self.text["state"] = "normal"
        self.text.delete("1.0", "end")
        self.text["state"] = "disabled"
        self.lower.grid_forget()
        self.higher.grid_forget()
        self.comparisonAnswer = answer
        self.displayEntry()


    def proceed(self):
        if self.state == "second":
            try:
                float(self.answerVar.get())
            except:
                self.warning["foreground"] = "red"
                return

        self.text["state"] = "normal"
        self.text.delete("1.0", "end")
        self.text["state"] = "disabled"
        self.answer.grid_forget()
        self.nextButton.grid_forget()

        if self.state == "first":
            self.root.texts[items[self.number][0]] = self.answerVar.get().replace("/t", " ").replace("\n", "\t")
            self.file.write("\t".join([self.id, items[self.number][0], self.valence,
                                       self.comparisonAnswer, self.answerVar.get().replace("/t", " ").replace("\n", "\t")]) + "\n")
        else:
            self.file.write("\t".join([self.id, items[self.number][0], self.comparisonAnswer, self.answerVar.get()]) + "\n")
        self.answerVar.set("")
        self.number += 1

        if self.number == len(items):
            self.nextFun()
        else:
            self.displayQuestion()

      

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([(Comparison, {"state": "first"}),
         (Comparison, {"state": "second"})
         ])
