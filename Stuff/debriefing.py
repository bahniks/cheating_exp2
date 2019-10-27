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

q1 = "V této a následující části máme zájem zjistit vaše názory na tento experiment. Prosím, napište svůj názor v několika bodech či větách."
q2 = "Máte nějaké připomínky k průběhu experimentu? Byly pokyny jasné? Bylo snadné sledovat uživatelské rozhraní? Máte nějaké připomínky týkající se chování experimentátorů? Existuje něco, co byste udělali jinak?"
q3 = "Jaký byl podle vašeho názoru cíl úkolu, ve kterém jste museli předpovídat, zda na kostce padne liché nebo sudé číslo? Uveďte prosím, proč jste se v této úloze zachovali tak, jak jste se zachovali."
q4 = "Myslíte si, že jste správně odhadli, co je v experimentu zkoumáno? Pakliže ano, snažili jste se vyjít vstříc záměru experimentátorů nebo jste se naopak chovali opačně?"
q5 = 'Myslíte si, že by bylo nemorální ve verzi "PO" uvádět větší počet správně uhodnutých hodů, abyste vydělali více peněz? Uveďte prosím také důvod své odpovědi.'
q6 = "Nakolik důvěřujete tomu, že všechny vám sdělené informace byly pravdivé?"
q6values = ["zcela důvěřuji", "spíše důvěřuji", "nejsem si jist", "spíše nedůvěřuji", "zcela nedůvěřuji"]

##################################################################################################################



class Debriefing(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.file.write("Debriefing\n")

        self.question1 = Question(self, q1, alines = 3)
        self.question2 = Question(self, q2, alines = 3, qlines = 3)
        self.question3 = Question(self, q3, alines = 3)
        self.question4 = Question(self, q4, alines = 3)
        self.question5 = Question(self, q5, alines = 3)
        self.question6 = Measure(self, q6, values = q6values, questionPosition = "above",
                                 left = "", right = "", labelPosition = "next")
        self.question6.question.grid(column = 0, row = 0, columnspan = 4, pady = 6)
        self.question6.question["font"] = "helvetica 15"

        self.question1.grid(row = 1, column = 1)
        self.question2.grid(row = 2, column = 1)
        self.question3.grid(row = 3, column = 1)
        self.question4.grid(row = 4, column = 1)
        self.question5.grid(row = 5, column = 1)
        self.question6.grid(row = 6, column = 1)
        
        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun)
        self.next.grid(row = 7, column = 1)

        self.warning = ttk.Label(self, text = "Odpovězte prosím na všechny otázky.",
                                 background = "white", font = "helvetica 15", foreground = "white")
        self.warning.grid(row = 8, column = 1)

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
        self.rowconfigure(8, weight = 1)
        self.rowconfigure(9, weight = 1)

        
    def check(self):
        return self.question1.check() and self.question2.check() and \
               self.question3.check() and self.question4.check() and \
               self.question5.check() and self.question6.answer.get()

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
        self.question5.write(newline = False)
        self.file.write("\t")
        self.question6.write()
        self.file.write("\n")

       
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

