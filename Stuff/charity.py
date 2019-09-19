#! python3
from tkinter import *
from tkinter import ttk

import os
import random

from common import ExperimentFrame
from gui import GUI
from constants import CURRENCY, WIN, COUNTRY


################################################################################
# TEXTS

charitiesChina = ["The Chinese Red Cross Foundation (红十字)",
                  "China Foundation for Poverty Alleviation (中国扶贫基金会)",
                  "One Foundation (壹基金)",
                  "China Charity Federation (中华慈善总会)"]
charitiesCzechia = ["Czech Red Cross (Červený kříž)",
                    "People in Need (Člověk v tísni)",
                    "Caritas Czech Republic (Charita Česká republika)",
                    "Barriers Account (Konto bariéry)"]

instructions = """
The set number {} was randomly selected in the dice rolling task.

You have therefore earned {} {}.

Now, you have an opportunity to give some of the earned money to a charity of your choice. 

Use the slider below to enter the amount you want to donate to one of the four charities listed below. In case you decide to donate some money, you can choose the charity by clicking the corresponding button.

It is completely up to you how much of your earned money you donate – you can donate any amount between 0 {} and the full earned amount. The donated amount will be deducted from your final payment for the study. The rest, that is the amount that you decide to keep, you will receive at the end of the study.

Our research team will send all the money collected to the chosen charities after the end of the data collection.
"""

donationtext = "Your donation is {} {}"



################################################################################


class Charity(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        selected = random.randint(1, 3)
        if "win" + str(selected) in self.root.texts:
            win = self.root.texts["win" + str(selected)]
        else:
            win = 5*WIN # for testing
        self.root.texts["dice"] = win           
      
        self.charity = StringVar()
        self.money = IntVar()
        self.money.set(0)

        self.text = Text(self, font = "helvetica 15", relief = "flat", background = "white", height = 15,
                         wrap = "word", highlightbackground = "white", width = 88)
        self.text.grid(row = 1, column = 0, columnspan = 4)
        self.text.insert("1.0", instructions.format(selected, win, CURRENCY, CURRENCY))
        self.text.config(state = "disabled")

        ttk.Style().configure("TScale", background = "white")

        self.scale = ttk.Scale(self, orient = HORIZONTAL, from_ = 0, to = win,
                               variable = self.money, command = self.changedScale)
        self.scale.grid(row = 2, column = 1, columnspan = 2, sticky = EW)

        self.donation = ttk.Label(self, text = donationtext.format(0, CURRENCY), background = "white",
                                  font = "helvetica 15")
        self.donation.grid(row = 3, column = 1, columnspan = 2, pady = 20)

        self.leftLabel = ttk.Label(self, text = "0 {}".format(CURRENCY), background = "white",
                                   font = "helvetica 15")
        self.leftLabel.grid(row = 2, column = 0, sticky = E, padx = 10)
        
        self.rightLabel = ttk.Label(self, text = "{} {}".format(win, CURRENCY), background = "white",
                                    font = "helvetica 16")
        self.rightLabel.grid(row = 2, column = 3, sticky = W, padx = 10)        

        if COUNTRY == "CHINA":
            charities = charitiesChina
        elif COUNTRY == "CZECHIA":
            charities = charitiesCzechia

        self.labels = {}
        self.rbuttons = {}
        for i, char in enumerate(charities):
            row = i + 4
            self.labels[i] = ttk.Label(self, text = char, background = "white", font = "helvetica 15")
            self.labels[i].grid(column = 1, row = row, pady = 2, sticky = W, padx = 20)
            self.rbuttons[i] = ttk.Radiobutton(self, text = "", variable = self.charity,
                                               value = char.split(" (")[0], command = self.checkCharity)
            self.rbuttons[i].grid(column = 2, row = row, sticky = W)

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 15")
        ttk.Style().configure("TButton", font = "helvetica 15")

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(3, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(9, weight = 1)
        self.rowconfigure(10, weight = 1)

        self.next = ttk.Button(self, text = "Continue", command = self.nextFun)
        self.next.grid(row = 9, column = 0, columnspan = 4, pady = 15)
        


    def changedScale(self, value):
        self.money.set(round(self.money.get(), 1))
        self.donation["text"] = donationtext.format(self.money.get(), CURRENCY)
        if self.money.get() and not self.charity.get():
            self.next["state"] = "disabled"
        else:
            self.next["state"] = "!disabled"


    def checkCharity(self):
        self.next["state"] = "!disabled"


    def write(self):
        self.file.write("Charity\n")
        if not self.charity.get():
            charity = "NA"
        else:
            charity = self.charity.get()
        self.root.texts["charity"] = charity
        self.root.texts["donation"] = self.money.get()
        self.file.write("\t".join([self.id, charity, str(self.money.get())]) + "\n")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Charity])
