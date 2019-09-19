#! python3
from tkinter import *
from tkinter import ttk
from time import perf_counter, sleep

import random
import os

from common import ExperimentFrame, InstructionsFrame, Measure
from gui import GUI




WIN = 35
CURRENCY = "Kč"



################################################################################
# TEXTS

continuetext = "Continue"
oddtext = "Odd (1,3,5)"
eventext = "Even (2,4,6)"
rolltext = "Roll a die"
correcttext = "Predicted correctly"
incorrecttext = "Predicted incorrectly"    
predictiontext = "I made a prediction."

treatmenttext = '''Trial {}

You have to decide whether an odd or even number will be rolled on a die in this trial. Now, please make your prediction, remember it, and then click on the button to roll the die.

Press "{}".
'''.format("{}", rolltext)

treatmenttext2 = "Select whether you predicted correctly and earned {} {} or whether you predicted incorrectly and earned nothing in this trial.".format(WIN, CURRENCY)

controltext = """Trial {}

You have to decide whether an odd or an even number will be rolled on a die in this trial. Now, select your prediction and then click on the button to roll the die.
"""

controltext2 = "In this trial, your prediction was {}"
wintext = "correct and you earned {} {}.".format(WIN, CURRENCY)
losstext = "incorrect and you earned nothing."

choicetext = """This is the end of the second set of 10 trials. If this set is chosen, you will receive {} {}.

As you have noticed, there were two versions of the task:

Version “BEFORE”, in which predictions are stated before the roll of a die. Afterwards, you see the outcome of the roll and learn whether your prediction was correct or not and how much you earned.
Version “AFTER”, in which you state whether your prediction was correct or incorrect and how much you earned after the roll of a die is made and you see its result.

Now, the last set of 10 trials is about to begin. You can choose which version of the task you want for the last set:
- BEFORE version  
- AFTER version
- select one of the two versions at random (that is, you will have 50% chance to get the BEFORE version and 50% chance to get the AFTER version of the task).
""".format("{}", CURRENCY)

# buttons
controlchoicetext = "BEFORE version"
treatmentchoicetext = "AFTER version"
randomchoicetext = "random selection"   

nochoicetext = """This is the end of the second set of 10 trials. If this set is chosen, you will receive {} {}.

As you have noticed, there were two versions of the task:

Version “BEFORE”, in which predictions are stated before the roll of a die. Afterwards, you see the outcome of the roll and learn whether your prediction was correct or not and how much you earned.
Version “AFTER”, in which you state whether your prediction was correct or incorrect and how much you earned after the roll of a die is made and you see its result.

Now, the last set of 10 trials is about to begin. For the last set, you were randomly assigned the {} of the task.
""".format("{}", CURRENCY, "{}")

firstversiontext = "BEFORE version"
secondversiontext = "AFTER version"

intro_block_1 = """
In the following task, you have to predict whether an odd or even number will be rolled on a virtual die on your computer. Numbers 1, 2, 3, 4, 5, and 6 can be rolled with equal probability. Odd numbers are 1, 3, and 5. Even numbers are 2, 4, and 6.

You will make predictions in 3 sets consisting of 10 trials each. There will be a short break after each set.

For every trial with a correct prediction, you earn {} {}.

After completing all three sets, one set will be chosen at random. You will only receive money earned in the chosen set. Therefore, if you make correct predictions in all 10 trials of a set that is later chosen, you will receive {} {}. The number of correct predictions in the two remaining sets does not affect the amount of money that you will receive in any way.

To check whether you understand the conditions correctly, please answer the following question:
When you make 7 correct predictions out of 10 in the first set, 5 correct predictions out of 10 in the second set, and 2 correct predictions out of 10 in the third set, and then the third set is chosen, how much money will you receive?
""".format(WIN, CURRENCY, WIN*10, CURRENCY)

wrong_answer = "{} {} is a wrong answer, the correct answer is {} {}. The third set was chosen and you correctly predicted 2 rolls in the third set. Therefore, you get 2×{} = {} {}.".format("{}", CURRENCY, WIN*2, CURRENCY, WIN, WIN*2, CURRENCY)
correct_answer = "{} {} is the correct answer. The third set was chosen and you correctly predicted 2 rolls in the third set. Therefore, you get 2×{} = {} {}.".format("{}", CURRENCY, WIN, WIN*2, CURRENCY)

second_check_question = "Before you begin, write down how many correct predictions you believe you will make in the chosen set for which you will earn money."
prediction_label = "correct predictions"
wrong_trials = "There are only 10 trials in one set!"

intro_block_2 = """
This is the end of the first set of 10 trials. If this set is chosen, you will receive {} {}. Now, the second block of 10 trials begins.
""".format("{}", CURRENCY)

endtext = """This is the end of the last set of 10 trials. If this set is chosen, you will receive {} {}.

This is the end of the dice rolling task.

""".format("{}", CURRENCY)

debrieftext = """
As was described before, the dice rolling task had two versions:

Version BEFORE, in which predictions are stated before the roll of a die. Afterwards, you see the outcome of the roll and learn whether your prediction was correct or not and how much you earned.

Version AFTER, in which you state whether your prediction was correct or incorrect and how much you earned after the roll of a die is made and you see its result.

Please rate how much do you agree or disagree with each of the following characterization for each version of the task.
"""

debriefquest1 = "How much do you agree that the BEFORE version of the task ..."
debriefquest2 = "How much do you agree that the AFTER version of the task ..."
debriefscale1 = "completely disagree"
debriefscale2 = "disagree"
debriefscale3 = "agree"
debriefscale4 = "completely agree"

debriefdimensions = ["... required attention",
                     "... required logical thinking",
                     "... enabled cheating",
                     "... made overreporting correct predictions acceptable",
                     "... the die roll was randomly generated"]



################################################################################


class Cheating(ExperimentFrame):
    def __init__(self, root, block):
        super().__init__(root)

        #######################
        # adjustable parameters
        self.trials = 10
        self.pause_after_roll = 0.5
        self.pause_before_trial = 0.2
        self.displayNum = self.createDots # self.createDots or self.createText
        self.fakeRolling = True # False for testing
        self.diesize = 240
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

        self.upperText.grid(column = 1, row = 1)
        self.upperButtonFrame.grid(column = 1, row = 2)
        self.die.grid(column = 1, row = 3, pady = 40)
        self.bottomText.grid(column = 1, row = 4)
        self.bottomButtonFrame.grid(column = 1, row = 5)
        self._createFiller()

        self["highlightbackground"] = "white"
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)
        self.rowconfigure(6, weight = 4)

        self.currentTrial = 0

        ttk.Style().configure("TButton", font = "helvetica 15")

        if block == 1:
            self.root.wins = [0, 0, 0]            

        self.responses = []


    def run(self):
        self.bottomText["state"] = "disabled"
        self.upperText["state"] = "disabled"
        if self.currentTrial < self.trials:
            self.currentTrial += 1
            self.startTrial()
        else:
            if self.blockNumber == 1:
                self.root.texts["win1"] = self.root.wins[0] * WIN
            elif self.blockNumber == 2:
                self.root.texts["win2"] = self.root.wins[1] * WIN
            elif self.blockNumber == 3:
                self.root.texts["win3"] = self.root.wins[2] * WIN
            self.nextFun()


    def startTrial(self):
        self.time = perf_counter()
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
            self.bottomText.insert("1.0", treatmenttext2)
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
            if win:
                self.root.wins[self.blockNumber - 1] += 1
            text = wintext if win else losstext
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


    def answer(self, answer = "NA"):
        t = perf_counter()
        if answer == "win":
            self.root.wins[self.blockNumber - 1] += 1
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
        self.update()
        sleep(self.pause_before_trial)
        self.run()
        
                   
    def write(self):
        for response in self.responses:
            begin = [self.id]
            self.file.write("\t".join(map(str, begin + response)) + "\n")



class Selection(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = choicetext, proceed = False, update = ["win2"], height = 17)

        ttk.Style().configure("TButton", font = "helvetica 15", width = 16)

        self.control = ttk.Button(self, text = controlchoicetext,
                                  command = lambda: self.response("control"))
        self.treatment = ttk.Button(self, text = treatmentchoicetext,
                                    command = lambda: self.response("treatment"))
        self.random = ttk.Button(self, text = randomchoicetext,
                                 command = lambda: self.response("random"))
        self.control.grid(row = 2, column = 0)
        self.random.grid(row = 2, column = 1)
        self.treatment.grid(row = 2, column = 2)        

    def response(self, choice):
        global conditions
        conditions[2] += "_" + choice
        if choice == "random":
            if random.random() < 0.5:
                conditions[2] += "_" + "treatment"
            else:
                conditions[2] += "_" + "control"
        self.nextFun()
       

        
class DebriefCheating(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.text = Text(self, height = 11, width = 90, relief = "flat", font = "helvetica 15", wrap = "word")
        self.text.insert("1.0", debrieftext)
        self.text["state"] = "disabled"
        self.text.grid(row = 1, column = 1)

        self.frame1 = OneFrame(self, debriefquest1)
        self.frame1.grid(row = 2, column = 1)

        self.frame2 = OneFrame(self, debriefquest2)
        self.frame2.grid(row = 3, column = 1)            

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = continuetext, command = self.nextFun,
                               state = "disabled")
        self.next.grid(row = 4, column = 1, sticky = N)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 2)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)

    def check(self):
        if self.frame1.check() and self.frame2.check():
            self.next["state"] = "!disabled"
            return True

    def write(self):
        if self.check():
            self.file.write("Perception cheating\n" + self.id + "\t")
            self.frame1.write()
            self.file.write("\t")
            self.frame2.write()
            self.file.write("\n")



class OneFrame(Canvas):
    def __init__(self, root, question):
        super().__init__(root, background = "white", highlightbackground = "white",
                         highlightcolor = "white")

        self.root = root
        self.file = self.root.file

        self.answers = [debriefscale1, debriefscale2, debriefscale3, debriefscale4]
        
        self.lab1 = ttk.Label(self, text = question, font = "helvetica 15", background = "white")
        self.lab1.grid(row = 2, column = 1, pady = 10)
        self.measures = []
        for count, word in enumerate(debriefdimensions):
            self.measures.append(Measure(self, word, self.answers, "", "", function = self.root.check,
                                         labelPosition = "none"))
            self.measures[count].grid(row = count + 3, column = 1, columnspan = 2, sticky = E)

    def check(self):
        for measure in self.measures:
            if not measure.answer.get():
                return False
        else:
            return True             

    def write(self):
        for num, measure in enumerate(self.measures):
            self.file.write(str(self.answers.index(measure.answer.get()) + 1))
            if num != len(self.measures) - 1:
                self.file.write("\t")
     


class CheatingInstructions(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = intro_block_1, height = 18, font = 16)

        self.predictionVar = StringVar()
        self.checkVar = StringVar()
        self.vcmd = (self.register(self.onValidate), '%P')
        self.checkFrame = Canvas(self, background = "white", highlightbackground = "white",
                                 highlightcolor = "white")
        self.checkFrame.grid(row = 2, column = 1)
        self.entry = ttk.Entry(self.checkFrame, textvariable = self.checkVar, width = 10, justify = "right",
                               font = "helvetica 16", validate = "key", validatecommand = self.vcmd)
        self.entry.grid(row = 2, column = 1, padx = 6)
        self.currencyLabel = ttk.Label(self.checkFrame, text = CURRENCY, font = "helvetica 16",
                                       background = "white")
        self.currencyLabel.grid(row = 2, column = 2, sticky = NSEW)

        self.lowerText = Text(self, font = "helvetica 16", relief = "flat", background = "white",
                              width = 90, height = 3, wrap = "word", highlightbackground = "white")
        self.lowerText.grid(row = 3, column = 1, pady = 15)
        self.lowerText["state"] = "disabled"

        self.bottomText = Text(self, font = "helvetica 16", relief = "flat", background = "white",
                               width = 90, height = 2, wrap = "word", highlightbackground = "white",
                               state = "disabled")
        self.bottomText.grid(row = 4, column = 1)
        self.bottomAnswers = Canvas(self, height = 40, background = "white", highlightbackground = "white",
                                    highlightcolor = "white")
        self.bottomAnswers.grid(row = 5, column = 1)
        self.predictionsLab = ttk.Label(self.bottomAnswers, text = prediction_label, font = "helvetica 16",
                                        background = "white", foreground = "white")
        self.predictionsLab.grid(row = 0, column = 1, sticky = NSEW, pady = 12)
        self.bottomMistakes = Text(self, font = "helvetica 16", relief = "flat", background = "white",
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
            if int(self.predictionVar.get()) > 10:
                self.bottomMistakes["state"] = "normal"
                self.bottomMistakes.delete("1.0", "end")
                self.bottomMistakes.insert("1.0", wrong_trials, "centered")
                self.bottomMistakes["state"] = "disabled"
                return
            self.write()
            super().nextFun()
        else:
            answer = int(self.checkVar.get())
            if answer == WIN*2:
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
        self.file.write("Cheating prediction\n")
        self.file.write(self.id + "\t" + self.predictionVar.get() + "\n\n")
        

        
conditions = ["treatment", "control"]
random.shuffle(conditions)
if random.random() < 0.5:
    if random.random() < 0.5:
        conditions.append("treatment")
    else:
        conditions.append("control")
else:
    conditions.append("choice")

Instructions1 = CheatingInstructions
Instructions2 = (InstructionsFrame, {"text": intro_block_2, "height": 5, "update": ["win1"]})
if conditions[2] == "choice":
    Instructions3 = Selection
else:
    addedtext = secondversiontext if conditions[2] == "treatment" else firstversiontext
    nochoicetext = nochoicetext.format("{}", addedtext)
    Instructions3 = (InstructionsFrame, {"text": nochoicetext, "height": 12, "update": ["win2"]})
BlockOne = (Cheating, {"block": 1})
BlockTwo = (Cheating, {"block": 2})
BlockThree = (Cheating, {"block": 3})

EndCheating = (InstructionsFrame, {"text": endtext, "height": 5, "update": ["win3"]})



if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Instructions1,
         BlockOne,
         Instructions2,
         BlockTwo,
         Instructions3,
         BlockThree,
         EndCheating,
         DebriefCheating
         ])
