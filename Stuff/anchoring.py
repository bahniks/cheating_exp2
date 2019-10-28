#! python3
from tkinter import *
from tkinter import ttk
from collections import deque
from time import perf_counter, sleep

import random
import os

from common import ExperimentFrame, InstructionsFrame
from gui import GUI



intro1 = """V následující části studie budete mezi sebou srovnávat různé hodnoty a uvádět příklady různých kategorií (např. příkladem nábytku by mohla být "židle").
Při uvádění příkladů uveďte vždy první příklad, co vás napadne. Dbejte nicméně na to, aby se opravdu jednalo o příklad dané kategorie.
"""

intro2 = """V následující části studie budete srovnávat a odhadovat různé hodnoty.
"""


items = [["price", "průměrná cena nového auta", "200 tisíc Kč", "900 tisíc Kč", "značky auta", "průměrná cena nového auta {}", "v tisících Kč"],
         ["temperature", "průměrná roční teplota v Praze", "1°C", "25°C", "měsíce v roce", "průměrná teplota v Praze v měsíci {}", "v °C"],
         ["age", "průměrný věk současného českého poslance/poslankyně", "25", "80", "současného českého poslance/poslankyně", "věk poslance/poslankyně jména {}", "v letech"],
         ["population", "průměrná populace států v EU", "1 milion obyvatel", "80 milionů obyvatel", "státu EU", "počet obyvatel státu {}", "v milionech obyvatel"],
         ["salary", "průměrná mzda v ČR", "15 000 Kč", "90 000 Kč", "zaměstnání", "průměrná mzda, kterou má {},", "v Kč"],
         ["distance", "průměrná vzdálenost hlavních měst evropských států od Prahy", "300 km", "2500 km", "hlavního města evropského státu (kromě Prahy)", "vzdálenost Prahy od města {}", "v km"],
         ["unemployment", "míra nezaměstnanosti v ČR", "1%", "10%", "kraje ČR", "míra nezaměstnanosti kraje {}", "v %"],
         ["weight", "průměrná hmotnost savce v pražské zoo", "1 kg", "3000 kg", "druhu savce", "hmotnost, kterou má {},", "v kg"],
         ["length", "průměrná délka českého křestního jména", "4 písmena", "9 písmen", "křestního jména", "délka jména {}", "počet písmen"],
         ["days", "průměrná délka oběhu planety sluneční soustavy okolo Slunce", "100 dní", "25 000 dní", "planety", "délka oběhu okolo Slunce planety {}", "ve dnech"]
         ]

random.shuffle(items)
#items = items[:2] # for testing


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
                         width = 80, height = 2, pady = 7, wrap = "word")
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
        
        self.rowconfigure(0, weight = 4)
        self.rowconfigure(1, weight = 4)
        self.rowconfigure(3, weight = 5)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 2)
        self.rowconfigure(6, weight = 10)

        self.number = 0

        if self.state == "first":
            self.displayQuestion()
        else:
            self.displayEntry()
        

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
            self.text.insert("end", self.question.format(items[self.number][5].format(self.root.texts[items[self.number][0]]),
                                                         items[self.number][1]), "center")
                                                         
        self.text["state"] = "disabled"

        self.lower.grid(row = 5, column = 1, sticky = E, padx = 20)
        self.higher.grid(row = 5, column = 2, sticky = W, padx = 20)


    def displayEntry(self):
        self.answer = ttk.Entry(self, textvariable = self.answerVar, font = "helvetica 20", width = 20)
        self.answer.grid(row = 4, column = 1, columnspan = 2, pady = 10)
        self.answer.bind("<KeyRelease>", self.checkEntry)
        self.nextButton.grid(row = 5, column = 1, columnspan = 2)
        self.nextButton["state"] = "disabled"
        self.text["state"] = "normal"
        if self.state == "first":
            sentenceEnd = items[self.number][4]
        else:
            sentenceEnd = items[self.number][1] + " ({})".format(items[self.number][6])       
        self.text.insert("end", self.entryInstruction.format(sentenceEnd), "center")
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
        if self.state == "first":
            self.displayEntry()
        elif self.state == "second":
            self.finishRound()
            

    def proceed(self):
        if self.state == "second":
            try:
                float(self.answerVar.get())
                self.warning["foreground"] = "white"
            except:
                self.warning["foreground"] = "red"
                return

        self.text["state"] = "normal"
        self.text.delete("1.0", "end")
        self.text["state"] = "disabled"
        self.answer.grid_forget()
        self.nextButton.grid_forget()
        if self.state == "first":
            self.finishRound()
        else:
            self.displayQuestion()


    def finishRound(self):
        if self.state == "first":
            self.root.texts[items[self.number][0]] = self.answerVar.get().replace("/t", " ").replace("\n", "\t")
            self.file.write("\t".join([self.id, str(self.number + 1), items[self.number][0], self.valence,
                                       self.comparisonAnswer, self.answerVar.get().replace("/t", " ").replace("\n", "\t")]) + "\n")
        else:
            self.file.write("\t".join([self.id, str(self.number + 1), items[self.number][0],
                                       self.comparisonAnswer, self.answerVar.get()]) + "\n")
        self.answerVar.set("")
        self.number += 1

        if self.number == len(items):
            self.nextFun()
        elif self.state == "first":
            self.displayQuestion()
        elif self.state == "second":
            self.displayEntry()



AnchoringInstructions1 = (InstructionsFrame, {"text": intro1, "height": 5, "font": 20})
AnchoringInstructions2 = (InstructionsFrame, {"text": intro2, "height": 3, "font": 20, "width": 60})
Comparison1 = (Comparison, {"state": "first"})
Comparison2 = (Comparison, {"state": "second"})
      

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([AnchoringInstructions1,
         Comparison1,
         AnchoringInstructions2,
         Comparison2
         ])
