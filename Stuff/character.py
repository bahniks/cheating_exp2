#! python3
from tkinter import *
from tkinter import ttk
from collections import deque
from time import perf_counter, sleep

import random
import os
import re

from common import ExperimentFrame, InstructionsFrame, Question, Measure
from gui import GUI
from common import read_all


intro = """
Následující úkol se týká usuzování o druhých lidech.
Postupně Vám popíšeme osm lidí. U každého člověka Vám ukážeme čtyři výroky, které o něm řekli jeho blízcí. Jedná se o výroky týkající se jeho aktivit, zvyků, ale i obyčejných zážitků a všedních činností. Následně vám popíšeme určitou situaci. Po vás budeme chtít, abyste na základě těchto informací zhodnotil(a), jaký postoj tento člověk má k životnímu prostředí a jestli dané chování poškozuje nebo chrání životní prostředí.
"""


intro2 = """
Nyní vám ukážeme znovu stejné informace o stejných osmi lidech. Tentokrát nás však bude zajímat, jak byste tohoto člověka a jeho chování hodnotil(a).
"""

CharacterIntro =(InstructionsFrame, {"text": intro, "height": 6})
CharacterIntro2 =(InstructionsFrame, {"text": intro2, "height": 6})


###########
n_items = 8 
###########

repeated_green = read_all("repeated_green.txt", encoding = None).split("\n")
repeated_filler = read_all("repeated_filler.txt", encoding = None).split("\n")
onetime_green = read_all("onetime_green.txt", encoding = None).split("\n")
onetime_filler = read_all("onetime_filler.txt", encoding = None).split("\n")
immoral = read_all("immoral.txt", encoding = None).split("\n")
immoral_short = read_all("immoral_short.txt", encoding = None).split("\n")
moral_short = read_all("moral_short.txt", encoding = None).split("\n")
names = read_all("names.txt", encoding = None).split("\n")

rd = [i for i in range(len(repeated_green))]
random.shuffle(rd)

random.shuffle(repeated_filler)
random.shuffle(onetime_filler)
random.shuffle(names)

repeated_green = [repeated_green[i] for i in rd[:4]]
onetime_green, moral = [onetime_green[i] for i in rd[4:8]], [onetime_green[i] for i in rd[8:12]]
moral_short = [moral_short[i] for i in rd[8:12]]
immoral = [immoral[i] for i in rd[12:16]]
immoral_short = [immoral_short[i] for i in rd[12:16]]

conditions = ["ffp", "fgp", "ggp", "gfp", "ffn", "fgn", "ggn", "gfn"]
random.shuffle(conditions)

shorts = []
texts = []
for i in range(n_items):
    text = []
    text.append(repeated_filler.pop()) 
    if conditions[i][0] == "f":
        text.append(repeated_filler.pop()) 
    else:
        text.append(repeated_green.pop()) 
    text.append(onetime_filler.pop()) 
    if conditions[i][1] == "f":
        text.append(onetime_filler.pop())
    else:
        text.append(onetime_green.pop())
    text = ['"' + t + '"' for t in text]
    random.shuffle(text)
    text = "\n\n".join(text)
    text += "\n\n\n"
    text += "Co se stalo:\n"
    if conditions[i][2] == "p":
        behavior = moral.pop()
        shorts.append(moral_short.pop())
    else:
        behavior = immoral.pop()
        shorts.append(immoral_short.pop())
    text += '"' + behavior + '"'
    text = text.replace("AAA", names[i])
    texts.append(text)


answers = ["Velmi nemorální", "Středně nemorální", "Spíše nemorální",
           "Spíše morální", "Středně morální", "Velmi morální"]
answers2 = ["Velmi negativní", "Středně negativní", "Spíše negativní",
            "Spíše pozitivní", "Středně pozitivní", "Velmi pozitivní"]


class Character(ExperimentFrame):
    def __init__(self, root, mode = "environment"):
        super().__init__(root)

        self.mode = mode

        self.file.write("Character {}\n".format(mode))

        self.nameVar = StringVar()

        self.name = ttk.Label(self, font = "helvetica 15 bold", textvariable = self.nameVar,
                              anchor = "center", background = "white")
        self.name.grid(row = 0, column = 2, pady = 15, sticky = S)
        
        self.text = Text(self, font = "helvetica 15", relief = "flat", background = "white",
                         width = 80, height = 18, pady = 7, wrap = "word")
        self.text.grid(row = 1, column = 1, columnspan = 3)
        self.text.tag_configure("bold", font = "helvetica 15 bold")
        
        ttk.Style().configure("TButton", font = "helvetica 16")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.answered, state = "disabled")
        self.next.grid(row = 4, column = 2)

        self.columnconfigure(0, weight = 3)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(3, weight = 1)
        self.columnconfigure(4, weight = 3)

        self.rowconfigure(0, weight = 2)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)

        self.order = -1
        self.initializeQuestions()
        self.proceed()
                 
    def proceed(self):
        self.order += 1
        if self.order == n_items:
            self.nextFun()
        else:
            self.text["state"] = "normal"
            self.text.delete("1.0", "end")
            self.text.insert("end", texts[self.order])
            i_index = self.text.search("Co se stalo:", "1.0")
            self.text.tag_add("bold", i_index, i_index + "+12c")
            self.text["state"] = "disabled"
            self.nameVar.set(names[self.order])
            self.newItem()
            self.next["state"] = "disabled"
            self.t0 = perf_counter()

    def initializeQuestions(self):
        if self.mode == "environment":
            self.q1 = "Jaký dopad na životní prostředí má to, že "
            ans = answers2
        else:    
            self.q1 = "Jak je podle Vašeho názoru morální to, že "
            ans = answers
        self.measure1 = Measure(self, self.q1, ans, "", "",
                                function = self.enable, questionPosition = "above")
        self.measure1.grid(row = 2, column = 1, columnspan = 3, pady = 10)

        if self.mode == "environment":
            self.q2 = "Jaký postoj má podle Vás AAA k ochraně životního prostředí?"
        else:
            self.q2 = "Jak je podle Vás AAA celkově morální nebo nemorální?"
        self.measure2 = Measure(self, self.q2, ans, "", "",
                                function = self.enable, questionPosition = "above")
        self.measure2.grid(row = 3, column = 1, columnspan = 3)

    def answered(self):
        self.file.write("\t".join([self.id, self.mode, self.measure1.answer.get(),
                                   self.measure2.answer.get(), conditions[self.order],
                                   "\t".join(re.findall(r'"(.*?)"', texts[self.order])),
                                   str(perf_counter() - self.t0)]) + "\n")
        self.proceed()
        
    def enable(self):
        if self.measure1.answer.get() and self.measure2.answer.get():
            self.next["state"] = "!disabled"

    def newItem(self):
        self.measure1.answer.set("")
        self.measure2.answer.set("")        
        self.measure1.question["text"] = self.q1 + shorts[self.order].replace("AAA", names[self.order]) + "?"
        self.measure2.question["text"] = self.q2.replace("AAA", names[self.order])
        

Character1 = (Character, {"mode": "environment"})
Character2 = (Character, {"mode": "character"})

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([CharacterIntro,
         Character1,
         CharacterIntro2,
         Character2       
         ])
