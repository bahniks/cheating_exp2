#! python3
from tkinter import *
from tkinter import ttk

import os
import random

from common import ExperimentFrame, InstructionsFrame
from gui import GUI

from constants import BONUS, CURRENCY


################################################################################
# TEXTS
questintro = """
In the following part of the study, you will answer several series of questions about yourself, your attitudes, and opinions. This part should take about 40 minutes. 

In order to check whether you pay attention to the questions, there are several attention checks mixed among the regular questions. You can earn an additional {} {} if you answer all of these checks correctly. 

Therefore, make sure to carefully read each question. However, try not to think too long about the questions – the first answer that comes into your mind is usually the best.

In case you do not understand all words in a question, try to answer to the best of your ability. Please do not ask research assistants for a clarification.
""".format(BONUS, CURRENCY)

hexacoinstructions = """On the following pages you will find a series of statements about you.
Please read each statement and decide how much you agree or disagree with that statement.
"""

agencyinstructions = "Please indicate the extent to which you agree with the following statements."

bidrinstructions = "Please read each statement and indicate how true it is."

workinstructions = "How comfortable would you feel about engaging in the following behaviors at work?"

attentiontext = "In order to prove that you are paying attention, select option "

################################################################################



class Quest(ExperimentFrame):
    def __init__(self, root, perpage, file, name, left, right, options = 5, shuffle = True,
                 instructions = "", height = 3, width = 80, center = False, checks = 0):
        super().__init__(root)

        self.perpage = perpage
        self.left = left
        self.right = right
        self.options = options
        self.checks = checks != 0
        self.name = name

        self.file.write("{}\n".format(name))

        if instructions:
            self.instructions = Text(self, height = height, relief = "flat", width = width,
                                     font = "helvetica 16", wrap = "word")
            self.instructions.grid(row = 1, column = 0, columnspan = 3)
            self.instructions.insert("1.0", instructions, "text")
            if center:
                self.instructions.tag_config("text", justify = "center") 
            self.instructions["state"] = "disabled"

        self.questions = []
        with open(os.path.join("Stuff", file)) as f:
            for line in f:
                self.questions.append(line.strip())

        if shuffle:
            random.shuffle(self.questions)

        if checks:
            spread = len(self.questions)//checks
            positions = [random.randint(self.perpage//2 + spread*i, spread*(i+1) - self.perpage//2) for \
                         i in range(checks)]
            for i in range(checks):
                self.questions.insert(positions[i], attentiontext + str(random.randint(1, options)) + ".")

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Continue", command = self.nextFun,
                               state = "disabled")
        self.next.grid(row = self.perpage*2 + 4, column = 1)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 2)
        self.rowconfigure(self.perpage*2 + 4, weight = 1)
        self.rowconfigure(self.perpage*2 + 5, weight = 3)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)

        self.mnumber = 0
        
        self.createQuestions()


    def createQuestions(self):
        self.measures = []
        for i in range(self.perpage):
            m = Likert(self, self.questions[self.mnumber], shortText = str(self.mnumber + 1),
                       left = self.left, right = self.right, options = self.options)
            m.grid(column = 0, columnspan = 3, row = i*2 + 3)
            self.rowconfigure(i*2 + 4, weight = 1)
            self.mnumber += 1
            self.measures.append(m)
            if self.mnumber == len(self.questions):
                break


    def nextFun(self):
        for measure in self.measures:
            measure.write()
            measure.grid_forget()
        if self.mnumber == len(self.questions):
            self.file.write("\n")
            if self.checks:
                self.file.write("Attention checks\n")
                wrong_checks = str(self.root.texts["attention_checks"])
                self.file.write(self.id + "\t" + self.name + "\t" + wrong_checks + "\n\n")
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



class Likert(Canvas):
    def __init__(self, root, text, options = 5, shortText = "",
                 left = "strongly disagree", right = "strongly agree"):
        super().__init__(root)

        self.root = root
        self.text = text
        self.short = shortText
        self.answer = StringVar()
        self["background"] = "white"
        self["highlightbackground"] = "white"
        self["highlightcolor"] = "white"

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 13")

        self.question = ttk.Label(self, text = text, background = "white",
                                  anchor = "center", font = "helvetica 14")
        self.question.grid(column = 0, row = 0, columnspan = options + 2, sticky = S)

        self.left = ttk.Label(self, text = left, background = "white",
                              font = "helvetica 13")
        self.right = ttk.Label(self, text = right, background = "white",
                               font = "helvetica 13")
        self.left.grid(column = 0, row = 1, sticky = E, padx = 5)
        self.right.grid(column = options + 1, row = 1, sticky = W, padx = 5)           

        for value in range(1, options + 1):
            ttk.Radiobutton(self, text = str(value), value = value, variable = self.answer,
                            command = self.check).grid(row = 1, column = value, padx = 4)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(options + 1, weight = 1)
        self.rowconfigure(0, weight = 1)


    def write(self):
        if attentiontext in self.text:
            if not "attention_checks" in self.root.root.texts:
                self.root.root.texts["attention_checks"] = 0
            if self.answer.get() != self.text[-2]:
                self.root.root.texts["attention_checks"] += 1
        else:
            ans = "{}\t{}\t{}\n".format(self.short, self.answer.get(), self.text.replace("\t", " "))
            self.root.file.write(self.root.id + "\t" + ans)


    def check(self):
        self.root.check()





class Hexaco(Quest):
    def __init__(self, root):
        super().__init__(root, 9, "hexaco.txt", "Hexaco", instructions = hexacoinstructions, width = 80,
                         left = "strongly disagree", right = "strongly agree", checks = 3,
                         height = 2, options = 5, center = True)

class BIDR(Quest):
    def __init__(self, root):
        super().__init__(root, 8, "BIDR.txt", "BIDR", instructions = bidrinstructions, center = True,
                         left = "not true", right = "very true", height = 1, options = 7)

class Agency(Quest):
    def __init__(self, root):
        super().__init__(root, 7, "agency.txt", "Moral agency", instructions = agencyinstructions, center = True,
                         left = "strongly disagree", right = "strongly agree", height = 1, options = 5)
        
class Disengagement(Quest):
    def __init__(self, root):
        super().__init__(root, 6, "disengagement.txt", "Moral disengagement", instructions = agencyinstructions,
                         left = "strongly disagree", right = "strongly agree",
                         height = 1, options = 7, center = True)

class Work(Quest):
    def __init__(self, root):
        super().__init__(root, 7, "work.txt", "Work deception", instructions = workinstructions,
                         left = "very uncomfortable", right = "very comfortable",
                         height = 1, options = 7, center = True)


QuestInstructions = (InstructionsFrame, {"text": questintro, "height": 13})


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([QuestInstructions,
         Hexaco,
         Work,
         BIDR,
         Agency,
         Disengagement
         ])
