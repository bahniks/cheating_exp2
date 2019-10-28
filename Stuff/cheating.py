#! python3
from tkinter import *
from tkinter import ttk
from time import perf_counter, sleep
from collections import defaultdict

import random
import os

from common import ExperimentFrame, InstructionsFrame, Measure
from gui import GUI
from debriefcheating import DebriefCheating




FEE = 25


################################################################################
# TEXTS

continuetext = "Pokračovat"
oddtext = "Liché (1, 3 nebo 5)"
eventext = "Sudé (2, 4 nebo 6)"
rolltext = "Hodit kostkou"
correcttext = "Správně"
incorrecttext = "Špatně"    
predictiontext = "Zvolil jsem si, že na kostce padne liché nebo sudé číslo"

treatmenttext = '''Kolo {}

Máte za úkol uhodnout, zda na kostce padne liché nebo sudé číslo. Nyní prosím zvolte, zda v následujícím hodě padne liché nebo sudé číslo, zapamatujte si svoji volbu a poté klikněte na tlačítko Hodit kostkou.
'''

treatmenttext2 = "Zvolte, zda jste správně uhodli a vydělali v tomto kole {} Kč nebo zda jste neuhodli a nevydělali jste v tomto kole nic."

controltext = """Kolo {}

Máte za úkol se uhodnout, zda na kostce padne liché nebo sudé číslo. Nyní prosím zvolte, zda v následujícím hodě padne liché nebo sudé číslo a poté klikněte na tlačítko Hodit kostkou.
"""

controltext2 = "V tomto kole byla vaše předpověď {}"
wintext = "správná a vydělali jste {} Kč."
losstext = "špatná a nevydělali jste možných {} Kč."


freetext = """Toto je konec {} bloku o dvanácti kolech. Pokud bude tento blok vylosován, obdržíte {} Kč.

Jak jste zaznamenali, úkol měl dvě verze:

Verzi “PŘED”, ve které činíte předpovědi před hodem kostkou. Po zvolení možnosti vidíte výsledek hodu a dozvíte se, zda jste uhodli či nikoliv, a kolik jste vydělali.
Verzi “PO”, ve které uvádíte, zda jste uhodli či nikoliv a kolik jste vydělali, až poté, co vidíte výsledek hodu kostkou.

Nyní vás čeká {} blok s dvanácti koly. Pro tento blok máte možnost si zvolit jednu z následujících možností:
- verze PŘED  
- verze PO.
"""

feetext = """Toto je konec {{}} bloku o dvanácti pokusech. Pokud bude tento blok vylosován, obdržíte {{}} Kč.

Jak jste zaznamenali, úkol měl dvě verze:

Verzi “PŘED”, ve které činíte předpovědi před hodem kostkou. Po zvolení možnosti vidíte výsledek hodu a dozvíte se, zda jste uhodli či nikoliv, a kolik jste vydělali.
Verzi “PO”, ve které uvádíte, zda jste uhodli či nikoliv a kolik jste vydělali, až poté, co vidíte výsledek hodu kostkou.

Nyní vás čeká {{}} blok s dvanácti pokusy. Pro tento blok máte opět možnost zvolit si jednu z uvedených verzí. Volba verze “PO” je ale zpoplatněna {} Kč. Zvolíte-li tuto verzi, bude částka {} Kč odečtena od výdělku v tomto bloku. Můžete si tedy zvolit jednu z následujících možností:
- verze PO a zaplatím {} Kč
- verze PŘED a zaplatím 0 Kč.
""".format(FEE, FEE, FEE)

# buttons
controlchoicetext = "verze PŘED"
treatmentchoicetext = "verze PO"  


intro_block_5 = """
Nyní vás čeká pátý, poslední blok s dvanácti koly. Úkol má opět dvě verze:

Verzi “PŘED”, ve které činíte předpovědi před hodem kostkou. Po zvolení možnosti vidíte výsledek hodu a dozvíte se, zda jste uhodli či nikoliv, a kolik jste vydělali.
Verzi “PO”, ve které uvádíte, zda jste uhodli či nikoliv a kolik jste vydělali, až poté, co vidíte výsledek hodu kostkou. Všimněte si, že za verzi “PO” v tomto bloku neplatíte žádný poplatek.

{}

Máte nyní poslední možnost zvolit si jednu z následujících možností:
- verze PŘED  
- verze PO.
"""

lowmanipulation = "V předchozím podobném experimentu si pouze 30 % účastníků zvolilo verzi “PO”."
highmanipulation = "V předchozím podobném experimentu si pouze 25 % účastníků zvolilo verzi “PŘED”."


estimatext = """
Toto je konec čtvrtého bloku o dvanácti kolech. Pokud bude tento blok vylosován, obdržíte {} Kč.

Jak jste zaznamenali, úkol měl dvě verze:

Verzi “PŘED”, ve které činíte předpovědi před hodem kostkou. Po zvolení možnosti vidíte výsledek hodu a dozvíte se, zda jste uhodli či nikoliv, a kolik jste vydělali.
Verzi “PO”, ve které uvádíte, zda jste uhodli či nikoliv a kolik jste vydělali, až poté, co vidíte výsledek hodu kostkou.

Odhadněte, 
- kolik % účastníků si zvolilo verzi “PŘED” a kolik hodů z 12 průměrně uhodli
- kolik % účastníků si zvolilo verzi “PO” a kolik hodů z 12 průměrně uhodli.

Ačkoli se při jednom rozhodnutí platil poplatek za verzi “PO”, nyní se ptáme na situaci, kdy za verzi “PO” žádný poplatek nebyl. 
"""

beforeEstimate = "% účastníků zvolilo verzi “PŘED” a uhodli průměrně"
afterEstimate = "% účastníků zvolilo verzi “PO” a uhodli průměrně"


intro_block_1 = """
V následujícím úkolu budete hádat, jestli na virtuální kostce (generátor náhodných čísel) na vašem počítači padne liché nebo sudé číslo. Každé z čísel 1, 2, 3, 4, 5 a 6 může padnout se stejnou pravděpodobností. Lichá čísla jsou 1, 3 a 5. Sudá čísla jsou jsou 2, 4 a 6. 

Úkol je rozdělen do pěti samostatných bloků a každý blok sestává z dvanácti kol. Bloky se odlišují pravidly, dle nichž budete hádat hody kostkou. Po každém bloku bude krátká přestávka.

Uhodnete-li hod v bloku, získáte 5 Kč, uhodnete-li další, získáte za něj dalších 10 Kč, uhodnete-li další hod, získáte za něj dalších 15 Kč a tak dále. Za každý další uhodnutý hod získáte navíc částku o 5 Kč vyšší, než byla předchozí odměna. Pokud tedy uhodnete všech 12 hodů, za poslední dvanáctý uhodnutý hod získáte 60 Kč a celkem získáte 390 Kč.

Poté, co dokončíte všech pět bloků, bude jeden blok náhodně vylosován. Obdržíte pouze peníze, které jste vydělali v tomto vylosovaném bloku. Pokud správně uhodnete všech dvanáct hodů v daném bloku, a tento blok bude později vylosován, obdržíte 390 Kč. Vaše výsledky v ostatních blocích nijak neovlivní množství peněz, které obdržíte.

Abychom ověřili, že rozumíte instrukcím, prosím odpovězte na následující otázku:
Když správně uhodnete 7 hodů z 12 v prvním bloku, 5 hodů z 12 ve druhém bloku, 2 hody z 12 ve třetím bloku a ve čtvrtém a pátém bloku neuhodnete žádný hod, a poté je vylosován třetí blok, kolik peněz obdržíte?
"""

wrong_answer = "{} Kč je chybná odpověď, správná odpověď je 15 Kč. Byl vylosován třetí blok, ve kterém jste správně uhodli 2 hody. Obdržíte tedy 5 + 10 = 15 Kč."
correct_answer = "15 Kč je správná odpověď. Byl vylosován třetí blok, ve kterém jste správně uhodli 2 hody. Obdržíte tedy 5 + 10 = 15 Kč."

second_check_question = "Dříve než začnete, zkuste odhadnout, kolik hodů správně uhodnete ve vylosovaném bloku."
prediction_label = "správných předpovědí"
wrong_trials = "V jednom kole je pouze 12 hodů!"


intro_block_2 = """
Toto je konec prvního bloku s dvanácti koly. Pokud bude tento blok vylosován, obdržíte {} Kč. Nyní začne druhý blok s dvanácti hody.
"""

endtext = """Toto je konec posledního bloku s dvanácti koly. Pokud bude tento blok vybrán, obdržíte {} Kč.

Toto je konec úkolu s kostkou.
"""

third = ("druhého", "třetí")
fourth = ("třetího", "čtvrtý")

winningInformation = """
V úloze s házením kostek byl náhodně vybrán blok {}.

Vyhráli jste proto {} Kč.
"""



################################################################################


class Cheating(ExperimentFrame):
    def __init__(self, root, block):
        super().__init__(root)

        #######################
        # adjustable parameters
        self.trials = 12 # change for testing
        self.pause_after_roll = 0.5
        self.pause_before_trial = 0.2
        self.displayNum = self.createDots # self.createDots or self.createText
        self.fakeRolling = True # False for testing
        self.diesize = 240
        self.rewards = [i*5 + 5 for i in range(self.trials)]
        #######################

        global conditions
        self.condition = conditions[block - 1]
        self.blockNumber = block

        self.width = self.root.screenwidth
        self.height = self.root.screenheight

        self.file.write("Cheating {}\n".format(block))

        self.upperText = Text(self, height = 5, width = 80, relief = "flat", font = "helvetica 15",
                              wrap = "word")
        self.upperButtonFrame = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                                       background = "white", height = 100)
        self.die = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                          background = "white", width = self.diesize, height = self.diesize)
        self.bottomText = Text(self, height = 3, width = 80, relief = "flat", font = "helvetica 15",
                               wrap = "word")
        self.bottomButtonFrame = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                                        background = "white", height = 100)

        self.infoWinnings = ttk.Label(self, text = "", font = "helvetica 15",
                                      background = "white", justify = "right")
        self.fillerLeft = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                                 background = "white", width = 200, height = 1)
        self.fillerRight = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                                  background = "white", width = 200, height = 1)
        self.infoWinnings.grid(row = 1, column = 2, sticky = NW)
        self.fillerLeft.grid(column = 0, row = 0)
        self.fillerRight.grid(column = 0, row = 0)

        self.upperText.grid(column = 1, row = 1)
        self.upperButtonFrame.grid(column = 1, row = 2)
        self.die.grid(column = 1, row = 3, pady = 40)
        self.bottomText.grid(column = 1, row = 4)
        self.bottomButtonFrame.grid(column = 1, row = 5)
        self._createFiller()

        self["highlightbackground"] = "white"
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)
        self.rowconfigure(6, weight = 4)

        self.currentTrial = 0

        ttk.Style().configure("TButton", font = "helvetica 15")

        if not hasattr(self.root, "wins"):
            self.root.wins = defaultdict(int)            

        self.responses = []


    def run(self):
        self.bottomText["state"] = "disabled"
        self.upperText["state"] = "disabled"
        if self.currentTrial < self.trials:
            self.currentTrial += 1
            self.startTrial()
        else:
            fee = FEE if conditions[self.blockNumber - 1] == "fee_treatment" else 0
            self.root.texts["win" + str(self.blockNumber)] = sum(self.rewards[:self.root.wins[self.blockNumber]]) - fee
            self.nextFun()


    def startTrial(self):
        self.time = perf_counter()
        self.showWinnings()
        self.upperPart()


    def _createFiller(self):
        self.fillerFrame = Canvas(self.bottomButtonFrame, highlightbackground = "white",
                                  highlightcolor = "white", background = "white", height = 100, width = 1)
        self.fillerFrame.grid(column = 0, row = 0, sticky = NS)


    def upperPart(self):
        self.upperText["state"] = "normal"
        if "treatment" in self.condition:
            ttk.Style().configure("TCheckbutton", background = "white", font = "helvetica 15")
            self.predictionVar = BooleanVar()
            self.predictionVar.set(False)
            self.upperText.insert("1.0", treatmenttext.format(self.currentTrial))
            self.predictedCB = ttk.Checkbutton(self.upperButtonFrame, text = predictiontext,
                                               command = self.checkbuttoned, variable = self.predictionVar,
                                               onvalue = True, offvalue = False)
            self.predictedCB.grid(row = 0, column = 1, pady = 15)
        elif "control" in self.condition:
            ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 15")
            self.predictionVar = StringVar()
            self.upperText.insert("1.0", controltext.format(self.currentTrial))
            self.evenButton = ttk.Radiobutton(self.upperButtonFrame, text = eventext, value = "even",
                                              variable = self.predictionVar, command = self.checked)
            self.oddButton = ttk.Radiobutton(self.upperButtonFrame, text = oddtext, value = "odd",
                                             variable = self.predictionVar, command = self.checked)
            self.evenButton.grid(row = 0, column = 2, padx = 10, pady = 15)
            self.oddButton.grid(row = 0, column = 0, padx = 10, pady = 15)

        self.rollButton = ttk.Button(self.upperButtonFrame, text = rolltext, command = self.roll,
                                     state = "disabled")
        self.rollButton.grid(row = 1, column = 1)
        self.upperText["state"] = "disabled"


    def checked(self):
        self.rollButton["state"] = "!disabled"
        self.oddButton["state"] = "disabled"
        self.evenButton["state"] = "disabled"


    def checkbuttoned(self):
        self.rollButton["state"] = "!disabled"
        self.predictedCB["state"] = "disabled"


    def bottomPart(self):
        self.bottomText["state"] = "normal"
        if "treatment" in self.condition:
            self.bottomText.insert("1.0", treatmenttext2.format(self.rewards[self.root.wins[self.blockNumber]]))
            ttk.Style().configure("Green.TButton", foreground = "green")
            ttk.Style().configure("Red.TButton", foreground = "red")
            self.winButton = ttk.Button(self.bottomButtonFrame, text = correcttext,
                                        command = lambda: self.answer("win"), width = 18, style = "Green.TButton")
            self.lossButton = ttk.Button(self.bottomButtonFrame, text = incorrecttext,
                                         command = lambda: self.answer("loss"), width= 18, style = "Red.TButton")
            self.winButton.grid(row = 0, column = 0, padx = 30)
            self.lossButton.grid(row = 0, column = 2, padx = 30)
        elif "control" in self.condition:
            win = (self.response == "odd" and self.currentRoll in (1,3,5)) or (
                self.response == "even" and self.currentRoll in (2,4,6))
            text = wintext if win else losstext
            text = text.format(self.rewards[self.root.wins[self.blockNumber]])
            if win:
                self.root.wins[self.blockNumber] += 1
            self.bottomText.insert("1.0", controltext2.format(text))
            self.continueButton = ttk.Button(self.bottomButtonFrame, text = continuetext,
                                             command = self.answer)
            self.continueButton.grid(row = 0, column = 1)
        self.bottomText["state"] = "disabled"


    def roll(self):
        self.firstResponse = perf_counter()
        if "treatment" in self.condition:
            self.response = "NA"    
        else:
            self.response = self.predictionVar.get()
        self.rollButton["state"] = "disabled"
        self.die.create_rectangle((5, 5, self.diesize - 5, self.diesize - 5),
                                  fill = "white", tag = "die", outline = "black", width = 5)
        # fake rolling
        if self.fakeRolling:
            for roll in range(random.randint(4,6)):         
                self.displayNum(self.diesize/2, self.diesize/2, random.randint(1, 6))
                self.update()
                sleep(0.2)
                self.die.delete("dots")
        self.currentRoll = random.randint(1, 6)
        self.displayNum(self.diesize/2, self.diesize/2, self.currentRoll)
        self.update()
        sleep(self.pause_after_roll)
        self.beforeSecondResponse = perf_counter()
        self.bottomPart()


    def createDots(self, x0, y0, num):
        positions = {"1": [(0,0)],
                     "2": [(-1,-1), (1,1)],
                     "3": [(-1,-1), (0,0), (1,1)],
                     "4": [(-1,-1), (-1,1), (1,-1), (1,1)],
                     "5": [(-1,-1), (-1,1), (0,0), (1,-1), (1,1)],
                     "6": [(-1,-1), (-1,1), (1,-1), (1,1), (-1,0), (1,0)]}
        for x, y in positions[str(num)]:
            d = self.diesize/4
            coords = [x0 + x*d + d/3, y0 - y*d + d/3,
                      x0 + x*d - d/3, y0 - y*d - d/3]
            self.die.create_oval(tuple(coords), fill = "black", tag = "dots")


    def createText(self, x0, y0, num):
        self.die.create_text(x0, y0, text = str(num), font = "helvetica 70", tag = "die")

    def showWinnings(self):
        fee = FEE if conditions[self.blockNumber - 1] == "fee_treatment" else 0
        self.infoWinnings["text"] = "Současná výhra:\n{} Kč".format(sum(self.rewards[:self.root.wins[self.blockNumber]]) - fee)

    def answer(self, answer = "NA"):
        t = perf_counter()
        if answer == "win":
            self.root.wins[self.blockNumber] += 1
        self.responses.append([self.blockNumber, self.currentTrial, self.condition,
                               self.currentRoll, self.response,
                               answer, t - self.time, self.firstResponse - self.time,
                               t - self.beforeSecondResponse])
        self.bottomText["state"] = "normal"
        self.upperText["state"] = "normal"
        self.die.delete("die")
        self.die.delete("dots")
        self.upperText.delete("1.0", "end")
        self.bottomText.delete("1.0", "end")
        for child in self.upperButtonFrame.winfo_children():
            child.grid_remove()
        for child in self.bottomButtonFrame.winfo_children():
            child.grid_remove()
        self._createFiller()
        self.showWinnings()
        self.update()
        sleep(self.pause_before_trial)
        self.run()
        
                   
    def write(self):
        for response in self.responses:
            begin = [self.id]
            self.file.write("\t".join(map(str, begin + response)) + "\n")



class Selection(InstructionsFrame):
    def __init__(self, root, roundNum, update = None):
        if 5 > roundNum > 2: 
            if conditions[roundNum - 1] == "fee":
                text = feetext
            else:
                text = freetext
            if roundNum == 3:
                text = text.format(third[0], "{}", third[1])
            elif roundNum == 4:
                text = text.format(fourth[0], "{}", fourth[1])
        elif roundNum == 5:
            manipulation = lowmanipulation if group == "low" else highmanipulation
            text = intro_block_5.format(manipulation)
            
        
        super().__init__(root, text = text, proceed = False, update = update, height = 17)

        self.roundNum = roundNum

        ttk.Style().configure("TButton", font = "helvetica 15", width = 16)

        self.control = ttk.Button(self, text = controlchoicetext,
                                  command = lambda: self.response("control"))
        self.treatment = ttk.Button(self, text = treatmentchoicetext,
                                    command = lambda: self.response("treatment"))
        self.control.grid(row = 2, column = 1, sticky = W)
        self.treatment.grid(row = 2, column = 1, sticky = E)

        self.columnconfigure(1, weight = 1)

    def response(self, choice):
        global conditions
        conditions[self.roundNum - 1] += "_" + choice
        self.nextFun()



class Estimate(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.text = Text(self, height = 17, font = "helvetica 18", wrap = "word", width = 80,
                         relief = "flat")
        self.text.insert("1.0", estimatext.format(self.root.texts["win4"]))
        self.text["state"] = "disabled"
        self.text.grid(column = 1, columnspan = 5, row = 1)

        self.beforePercVar = StringVar()
        self.afterPercVar = StringVar()
        self.beforeRollsVar = StringVar()
        self.afterRollsVar = StringVar()
        
        self.percEntryBefore = ttk.Entry(self, textvariable = self.beforePercVar, width = 5,
                                         justify = "right", font = "helvetica 18")
        self.percEntryAfter = ttk.Entry(self, textvariable = self.afterPercVar, width = 5,
                                        justify = "right", font = "helvetica 18")
        self.labelBefore = ttk.Label(self, text = beforeEstimate, font = "helvetica 18", background = "white")
        self.labelAfter = ttk.Label(self, text = afterEstimate, font = "helvetica 18", background = "white")
        self.rollsEntryBefore = ttk.Entry(self, textvariable = self.beforeRollsVar, width = 5,
                                          justify = "right", font = "helvetica 18")
        self.rollsEntryAfter = ttk.Entry(self, textvariable = self.afterRollsVar, width = 5,
                                         justify = "right", font = "helvetica 18")
        self.roolsBefore = ttk.Label(self, text = "hodů", font = "helvetica 18", background = "white")
        self.roolsAfter = ttk.Label(self, text = "hodů", font = "helvetica 18", background = "white")

        self.percEntryBefore.bind("<KeyRelease>", self.checkEntry)
        self.percEntryAfter.bind("<KeyRelease>", self.checkEntry)
        self.rollsEntryBefore.bind("<KeyRelease>", self.checkEntry)
        self.rollsEntryAfter.bind("<KeyRelease>", self.checkEntry)
                        
        self.percEntryBefore.grid(column = 1, row = 3, pady = 10, sticky = E, padx = 10)
        self.percEntryAfter.grid(column = 1, row = 4, sticky = E, padx = 10)
        self.labelBefore.grid(column = 2, row = 3, pady = 10)
        self.labelAfter.grid(column = 2, row = 4)
        self.rollsEntryBefore.grid(column = 3, row = 3, pady = 10, padx = 10)
        self.rollsEntryAfter.grid(column = 3, row = 4, padx = 10)
        self.roolsBefore.grid(column = 4, row = 3, pady = 10)
        self.roolsAfter.grid(column = 4, row = 4)

        self.warning = ttk.Label(self, text = "\n", font = "helvetica 18",
                                 background = "white", foreground = "white", justify = "center", state = "disabled")
        self.warning.grid(row = 5, column = 1, columnspan = 5)

        ttk.Style().configure("TButton", font = "helvetica 18", width = 12)

        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun, state = "disabled")
        self.next.grid(column = 1, columnspan = 5, row = 6, sticky = N)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(5, weight = 1)
        self.columnconfigure(6, weight = 1)
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(5, weight = 1)
        self.rowconfigure(6, weight = 2)

    def check(self):
        try:
            float(self.beforePercVar.get())
            float(self.afterPercVar.get())
            float(self.beforeRollsVar.get())
            float(self.afterRollsVar.get())
            if abs(float(self.beforePercVar.get()) + float(self.afterPercVar.get()) - 100) > 0.1:
                self.warning["text"] = "Součet pravděpodobností se musí rovnat 100%\n"
                self.warning["foreground"] = "red"
                return False
            elif float(self.beforeRollsVar.get()) > 12 or float(self.afterRollsVar.get()) > 12:
                self.warning["text"] = "V jednom bloku je pouze 12 kol\n"
                self.warning["foreground"] = "red"                
            else: 
                return True            
        except Exception:
            self.warning["text"] = "Odpověď musí být číslo!\n(pro desetinná místa u procent použijte tečku)"
            self.warning["foreground"] = "red"
            return False

              
    def checkEntry(self, e):           
        if all([self.beforePercVar.get(), self.afterPercVar.get(),
                self.beforeRollsVar.get(), self.afterRollsVar.get()]):
            self.next["state"] = "!disabled"
        else:
            self.next["state"] = "disabled"

    def write(self):
        self.file.write("Cheating predictions\n")
        self.file.write("\t".join([self.id, self.beforePercVar.get(), self.afterPercVar.get(),
                                   self.beforeRollsVar.get(), self.afterRollsVar.get()]) + "\n")
                
       
    

class CheatingInstructions(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = intro_block_1, height = 23, font = 15)

        self.predictionVar = StringVar()
        self.checkVar = StringVar()
        self.vcmd = (self.register(self.onValidate), '%P')
        self.checkFrame = Canvas(self, background = "white", highlightbackground = "white",
                                 highlightcolor = "white")
        self.checkFrame.grid(row = 2, column = 1)
        self.entry = ttk.Entry(self.checkFrame, textvariable = self.checkVar, width = 10, justify = "right",
                               font = "helvetica 15", validate = "key", validatecommand = self.vcmd)
        self.entry.grid(row = 2, column = 1, padx = 6)
        self.currencyLabel = ttk.Label(self.checkFrame, text = "Kč", font = "helvetica 16",
                                       background = "white")
        self.currencyLabel.grid(row = 2, column = 2, sticky = NSEW)

        self.lowerText = Text(self, font = "helvetica 15", relief = "flat", background = "white",
                              width = 90, height = 3, wrap = "word", highlightbackground = "white")
        self.lowerText.grid(row = 3, column = 1, pady = 15)
        self.lowerText["state"] = "disabled"

        self.bottomText = Text(self, font = "helvetica 15", relief = "flat", background = "white",
                               width = 90, height = 2, wrap = "word", highlightbackground = "white",
                               state = "disabled")
        self.bottomText.grid(row = 4, column = 1)
        self.bottomAnswers = Canvas(self, height = 40, background = "white", highlightbackground = "white",
                                    highlightcolor = "white")
        self.bottomAnswers.grid(row = 5, column = 1)
        self.predictionsLab = ttk.Label(self.bottomAnswers, text = prediction_label, font = "helvetica 15",
                                        background = "white", foreground = "white")
        self.predictionsLab.grid(row = 0, column = 1, sticky = NSEW, pady = 12)
        self.bottomMistakes = Text(self, font = "helvetica 15", relief = "flat", background = "white",
                                   width = 90, height = 1, wrap = "word", highlightbackground = "white",
                                   state = "disabled", foreground = "red")
        self.bottomMistakes.tag_config("centered", justify = "center")
        self.bottomMistakes.grid(row = 6, column = 1, pady = 10)
        
        self.next.grid(row = 7, column = 1)
        self.next["state"] = "disabled"
        self.text.grid(row = 1, column = 1, columnspan = 1)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(2, weight = 0)
        self.rowconfigure(3, weight = 0)
        self.rowconfigure(7, weight = 1)
        self.rowconfigure(8, weight = 2)

        self.checked = False
        
    def onValidate(self, P):
        try:
            if int(P) >= 0:
                self.next["state"] = "!disabled"
            else:
                self.next["state"] = "disabled"
        except Exception as e:
            self.next["state"] = "disabled"
        return True
    
    def nextFun(self):
        if self.checked:
            if int(self.predictionVar.get()) > 12:
                self.bottomMistakes["state"] = "normal"
                self.bottomMistakes.delete("1.0", "end")
                self.bottomMistakes.insert("1.0", wrong_trials, "centered")
                self.bottomMistakes["state"] = "disabled"
                return
            self.write()
            super().nextFun()
        else:
            answer = int(self.checkVar.get())
            if answer == 15:
                text = correct_answer.format(answer)
            else:
                text = wrong_answer.format(answer)
            self.lowerText["state"] = "normal"
            self.lowerText.insert("1.0", text)
            self.lowerText["state"] = "disabled"
            self.next["state"] = "disabled"
            self.checked = True
            self.bottomText["state"] = "normal"
            self.bottomText.insert("1.0", second_check_question)
            self.bottomText["state"] = "disabled"
            self.vcmd2 = (self.register(self.onValidate), '%P')
            self.predictionsEntry = ttk.Entry(self.bottomAnswers, textvariable = self.predictionVar, width = 10,
                                              justify = "right", font = "helvetica 16", validate = "key",
                                              validatecommand = self.vcmd2)
            self.predictionsLab["foreground"] = "black"
            self.predictionsEntry.grid(row = 0, column = 0, padx = 6)

    def write(self):
        self.file.write("Cheating estimates\n")
        self.file.write(self.id + "\t" + self.predictionVar.get() + "\n\n")
        

        
conditions = ["treatment", "control"]
conditions2 = ["free", "fee"]
random.shuffle(conditions)
random.shuffle(conditions2)
conditions = conditions + conditions2
group = random.choice(["low", "high"])
conditions += [group]


Instructions1 = CheatingInstructions
Instructions2 = (InstructionsFrame, {"text": intro_block_2, "height": 5, "update": ["win1"]})
Instructions3 = (Selection, {"roundNum": 3, "update": ["win2"]})
Instructions4 = (Selection, {"roundNum": 4, "update": ["win3"]})
Instructions5 = (Selection, {"roundNum": 5})

BlockOne = (Cheating, {"block": 1})
BlockTwo = (Cheating, {"block": 2})
BlockThree = (Cheating, {"block": 3})
BlockFour = (Cheating, {"block": 4})
BlockFive = (Cheating, {"block": 5})

EndCheating = (InstructionsFrame, {"text": endtext, "height": 5, "update": ["win5"]})


class Winning(InstructionsFrame):
    def __init__(self):
        pass

    def __call__(self, root):
        win = random.randint(1, 5)
        root.texts["dice"] = root.texts["win{}".format(win)]
        text = winningInformation.format(win, root.texts["dice"])        
        super().__init__(root, text, height = 5)
        return self

winning = Winning()



if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Instructions1,
         BlockOne,
         Instructions2,
         BlockTwo,
         Instructions3,
         BlockThree,
         Instructions4,
         BlockFour,
         Estimate,
         Instructions5,
         BlockFive,
         EndCheating,
         winning,
         DebriefCheating
         ])
