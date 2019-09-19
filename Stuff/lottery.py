#! python3
from tkinter import *
from tkinter import ttk

import os
import random

from collections import OrderedDict

from common import ExperimentFrame, InstructionsFrame
from gui import GUI
from constants import CURRENCY, WIN, COUNTRY


################################################################################
# TEXTS

optionsChina = ((12, 13, 14, 15, 16),
                (30, 40, 50, 60, 70),
                (30, 30, 30, 30, 30))
optionsCzechia = ((42, 44, 46, 48, 50),
                  (30, 40, 50, 60, 70),
                  (100, 100, 100, 100, 100))

instructions = """
In the following task, you will have to make 5 separate decisions between two alternatives each. First alternative always represents a sure payoff, second alternative represents a lottery. The % number represents the probability that you win and your payoff will then be {} {}. If you do not win, your payoff will be 0 {}. The payoff probabilities vary across the decisions so that the riskier alternative (i.e. lottery) is increasingly attractive with each row. 

After you have completed this task, your payoff will be determined. For this, one of your decisions will be selected at random (with equal probabilities) and you will get a certain payoff or the corresponding lottery will be played (based on whether you have chosen a sure payoff or a lottery). Thus, although you will have made five choices, only one eventually determines your payoff.

Please select in each row whether you prefer a sure payoff or a lottery.
"""

wintext = """
Your decision number {} was selected randomly.

{}
"""

sure = "Because you have chosen a sure payoff, you win {} {}."
risky = "Because you have chosen a lottery, the draw has taken place and you win {} {}."


################################################################################


class Lottery(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        if COUNTRY == "CHINA":
            options = optionsChina
        elif COUNTRY == "CZECHIA":
            options = optionsCzechia
        self.options = options
           
        self.text = Text(self, font = "helvetica 15", relief = "flat", background = "white", height = 14,
                         wrap = "word", highlightbackground = "white", width = 90)
        self.text.grid(row = 1, column = 0, columnspan = 4)
        self.text.insert("1.0", instructions.format(options[2][0], CURRENCY, CURRENCY))
        self.text.config(state = "disabled")

        self.leftLabel = ttk.Label(self, text = "Sure payoff", font = "helvetica 15", background = "white")
        self.leftLabel.grid(row = 3, column = 1, pady = 10)
        self.rightLabel = ttk.Label(self, text = "Lottery", font = "helvetica 15", background = "white")
        self.rightLabel.grid(row = 3, column = 2, pady = 10)

        self.variables = OrderedDict()
        self.rbuttonsL = {}
        self.rbuttonsR = {}
        for i in range(5):
            row = i + 4
            self.variables[i] = StringVar()
            self.rbuttonsL[i] = ttk.Radiobutton(self, text = " {} {}".format(options[0][i], CURRENCY),
                                                variable = self.variables[i], value = str(i+1) + "sure",
                                                command = self.checkAllFilled)
            self.rbuttonsL[i].grid(column = 1, row = row, sticky = W, padx = 30)
            self.rbuttonsR[i] = ttk.Radiobutton(self, variable = self.variables[i], value = str(i+1) + "risky",
                                                text = " {}% {} {}".format(options[1][i], options[2][i], CURRENCY),
                                                command = self.checkAllFilled)
            self.rbuttonsR[i].grid(column = 2, row = row, sticky = W, padx = 30)

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
        self.next["state"] = "disabled"
        

    def checkAllFilled(self):
        if all([var.get() for var in self.variables.values()]):
            self.next["state"] = "!disabled"


    def write(self):
        selected = random.randint(1, 5)
        self.root.texts["lottery_selected"] = selected
        if "risky" in self.variables[selected - 1].get():
            self.root.texts["lottery_chosen"] = "risky"
            if random.random() * 100 < self.options[1][selected - 1]:
                win = self.options[2][selected - 1]
                self.root.texts["lottery_random"] = "won"
            else:
                win = 0
                self.root.texts["lottery_random"] = "lost"
        else:
            self.root.texts["lottery_chosen"] = "safe"
            win = self.options[0][selected - 1]
        self.file.write("Lottery\n")
        self.root.texts["lottery_win"] = win
        self.file.write("\t".join([self.id] + [var.get() for var in self.variables.values()]) + "\n")



class LotteryWin(InstructionsFrame):
    def __init__(self, root):
        self.root = root
        if self.root.texts["lottery_chosen"] == "risky":
            append = risky
        else:
            append = sure
        text = wintext.format(self.root.texts["lottery_selected"],
                              append.format(self.root.texts["lottery_win"], CURRENCY))       
        super().__init__(root, text = text, proceed = True, height = 5)  


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Lottery,
         LotteryWin])
