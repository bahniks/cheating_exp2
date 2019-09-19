#! python3
from tkinter import *
from tkinter import ttk

import os

from math import ceil

from common import ExperimentFrame
from gui import GUI
from constants import COUNTRY, CURRENCY, BONUS, ROUNDING, EXCHANGE_RATE


##################################################################################################################
# TEXTS #
#########

english_level = ["No knowledge of English",
                 "Elementary level of English (KET level)",
                 "Low intermediate level of English (PET level)",
                 "High intermediate level of English (FCE level)",
                 "Advanced level of English (CAE level)",
                 "Proficient in English (CPE level)"]
english_china = ["No knowledge of English",
                 "Elementary level of English (IELTS below 4.5)",
                 "Low intermediate level of English (IELTS 4.0-4.5)",
                 "High intermediate level of English (IELTS 5.0-6.5)",
                 "Advanced level of English (IELTS 7.0-8.0)",
                 "Proficient in English (IELTS 8.5-9.0)"]
education_levels = ["None",
                    "Primary school",
                    "Middle school",
                    "High school",
                    "Technical high school",
                    "University",
                    "Technical college",
                    "Master degree",
                    "Doctoral degree"]
education_field = ["I have not studied university",
                   "Natural and Physical Sciences",
                   "Information Technology",
                   "Engineering and Related Technologies",
                   "Architecture and Building",
                   "Agriculture, Environmental and Related Studies",
                   "Health",
                   "Education",
                   "Management and Commerce",
                   "Society and Culture",
                   "Creative Arts",
                   "Food, Hospitality and Personal Services",
                   "Other"]
working_experience = ["Yes, I have worked or I am working full-time",
                      "Yes, I have worked or I am working part-time",
                      "No, I have worked or I am working only as a freelancer",
                      "No, I only had short-term holiday jobs, internships or fellowships",
                      "No, I have not worked in any organization yet"]
positions = ["social worker", "farmer", "therapist/psychologist", "artist",
             "IT engineer", "scientist", "civil servant", "craftsmen/craftswomen",
             'lawyer', 'media personality (TV, radio, Youtube etc.)', 'journalist',
             'police officer', 'clergy', 'salesperson', 'advertiser', 'investment banker',
             'lobbyist', 'politician', 'management consultant', 'non-profit employee',
             'author (novelist, writer etc.)', 'accountant', 'auditor', 'physician', 'judge',
             'university professor', 'teacher', 'nurse', 'engineer']

education_question = "What is the highest diploma or certificate you have obtained?"
language_question = "What is your level of English proficiency?"
experience_question = "Do you have a work experience in a company or an organization?"
field_question = "If you have studied a university, what field have you studied?"
position_question = "What is your preferred profession (select the closest):"
sex_question = "Sex: "
age_question = "What is your age: "
nationality_question = "Nationality:  "

##################################################################################################################


class Demographics(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 15")
        ttk.Style().configure("TButton", font = "helvetica 15")
       
        self.sex = StringVar()
        self.age = StringVar()
        self.nationality = StringVar()
        self.language = StringVar()
        self.education = StringVar()
        self.field = StringVar()
        self.field.set(education_field[0])
        self.experience = StringVar()
        self.position = StringVar()

        self.lab1 = ttk.Label(self, text = sex_question, background = "white",
                              font = "helvetica 15")
        self.lab1.grid(column = 1, row = 1, pady = 2, sticky = W, padx = 2)
        self.lab2 = ttk.Label(self, text = age_question, background = "white",
                              font = "helvetica 15")
        self.lab2.grid(column = 1, row = 2, pady = 2, sticky = W, padx = 2)        
        self.lab3 = ttk.Label(self, text = nationality_question, background = "white",
                              font = "helvetica 15")
        self.lab3.grid(column = 1, row = 3, pady = 2, sticky = W, padx = 2)
        self.lab4 = ttk.Label(self, text = language_question, background = "white",
                              font = "helvetica 15")
        self.lab4.grid(column = 1, row = 4, pady = 2, sticky = W, padx = 2)
        self.lab5 = ttk.Label(self, text = education_question, background = "white",
                              font = "helvetica 15")
        self.lab5.grid(column = 1, row = 5, pady = 2, sticky = W, padx = 2)
        self.lab6 = ttk.Label(self, text = field_question, background = "white",
                              font = "helvetica 15")
        self.lab6.grid(column = 1, row = 6, pady = 2, sticky = W, padx = 2)
        self.lab7 = ttk.Label(self, text = experience_question, background = "white",
                              font = "helvetica 15")
        self.lab7.grid(column = 1, row = 7, pady = 2, sticky = W, padx = 2)
        self.lab8 = ttk.Label(self, text = position_question, background = "white",
                              font = "helvetica 15")
        self.lab8.grid(column = 1, row = 8, pady = 2, sticky = W, padx = 2)
   
        self.male = ttk.Radiobutton(self, text = "male", variable = self.sex, value = "male",
                                    command = self.checkAllFilled)
        self.female = ttk.Radiobutton(self, text = "female", variable = self.sex,
                                      value = "female", command = self.checkAllFilled)   

        self.ageCB = ttk.Combobox(self, textvariable = self.age, width = 6, font = "helvetica 14",
                                  state = "readonly")
        self.ageCB["values"] = tuple([""] + [str(i) for i in range(18, 80)])
        self.ageCB.bind("<<ComboboxSelected>>", lambda e: self.checkAllFilled())

        if COUNTRY == "CHINA":
            nationality_name = "chinese"
        else:
            nationality_name = "czech"
        self.nationalityRB = ttk.Radiobutton(self, text = nationality_name, variable = self.nationality,
                                             value = nationality_name, command = self.checkAllFilled)
        self.other = ttk.Radiobutton(self, text = "other", variable = self.nationality,
                                     value = "other", command = self.checkAllFilled)

        self.languageCB = ttk.Combobox(self, textvariable = self.language, width = 35,
                                       font = "helvetica 14", state = "readonly")
        if COUNTRY == "CHINA":
            self.languageCB["values"] = english_china
        else:
            self.languageCB["values"] = english_level
        self.languageCB.bind("<<ComboboxSelected>>", lambda e: self.checkAllFilled()) 

        self.educationCB = ttk.Combobox(self, textvariable = self.education, width = 30,
                                    font = "helvetica 14", state = "readonly")
        self.educationCB["values"] = education_levels
        self.educationCB.bind("<<ComboboxSelected>>", lambda e: self.checkAllFilled())

        self.fieldCB = ttk.Combobox(self, textvariable = self.field, width = 25,
                                    font = "helvetica 14", state = "readonly")
        self.fieldCB["values"] = education_field
        self.fieldCB.bind("<<ComboboxSelected>>", lambda e: self.checkAllFilled())

        self.experienceCB = ttk.Combobox(self, textvariable = self.experience, width = 50,
                                       font = "helvetica 14", state = "readonly")
        self.experienceCB["values"] = working_experience
        self.experienceCB.bind("<<ComboboxSelected>>", lambda e: self.checkAllFilled())        

        self.positionCB = ttk.Combobox(self, textvariable = self.position, width = 25,
                                       font = "helvetica 14", state = "readonly")
        self.positionCB["values"] = positions
        self.positionCB.bind("<<ComboboxSelected>>", lambda e: self.checkAllFilled()) 

        self.male.grid(column = 2, row = 1, pady = 7, padx = 7, sticky = W)
        self.female.grid(column = 3, row = 1, pady = 7, padx = 7, sticky = W)
        self.ageCB.grid(column = 2, row = 2, pady = 7, padx = 7, sticky = W)
        self.nationalityRB.grid(column = 2, row = 3, pady = 7, padx = 7, sticky = W)
        self.other.grid(column = 3, row = 3, pady = 7, padx = 7, sticky = W)
        self.languageCB.grid(column = 2, columnspan = 3, row = 4, pady = 7, padx = 7, sticky = W)
        self.educationCB.grid(column = 2, columnspan = 3, row = 5, pady = 7, padx = 7, sticky = W)
        self.fieldCB.grid(column = 2, columnspan = 3, row = 6, pady = 7, padx = 7, sticky = W)
        self.experienceCB.grid(column = 2, columnspan = 3, row = 7, pady = 7, padx = 7, sticky = W)
        self.positionCB.grid(column = 2, columnspan = 2, row = 8, pady = 7, padx = 7, sticky = W)

        self.columnconfigure(5, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(11, weight = 1)

        self.writeWinnings()

        self.next = ttk.Button(self, text = "Continue", command = self.nextFun,
                               state = "disabled")
        self.next.grid(row = 11, column = 1, pady = 15, columnspan = 3)


    def checkAllFilled(self, _ = None):
        if all([v.get() for v in [self.sex, self.age, self.nationality, self.language,
                                  self.education, self.field, self.experience, self.position]]):
            self.next["state"] = "!disabled"


    def writeWinnings(self):
        options = os.path.join(os.path.dirname(os.path.dirname(__file__)), "options.txt")
        if os.path.exists(options):
            with open(options, mode = "r") as f:
                directory = f.readline().strip()
                station = f.readline().strip()
            if not os.path.exists(directory):
                directory = os.path.dirname(self.root.outputfile)
        else:
            directory = os.path.dirname(self.root.outputfile)
            station = "UNKNOWN"
        self.root.texts["station"] = station
        filename = os.path.splitext(os.path.basename(self.root.outputfile))[0]
        output = os.path.join(directory, filename + "_STATION_" + str(station) + ".txt")
        if all([key in self.root.texts for key in ["dice", "charity", "donation",
                                                   "lottery_win", "attention_checks"]]):
            if self.root.texts["attention_checks"] > 0:
                self.root.texts["attention1"] = " not"
                self.root.texts["attention2"] = "did not earn"
            else:
                self.root.texts["attention1"] = ""
                self.root.texts["attention2"] = "earned"
            dice = self.root.texts["dice"]
            charity = self.root.texts["charity"]
            donation = self.root.texts["donation"]
            lottery = self.root.texts["lottery_win"]
            bonus = 0 if self.root.texts["attention_checks"] else BONUS
            with open(output, mode = "w", encoding = "utf-8") as infile:
                reward = dice + lottery + bonus - donation
                self.root.texts["reward"] = reward
                if ROUNDING:
                    reward = ceil((reward)/85)*100
                    self.root.texts["rounded_reward"] = reward
                if COUNTRY == "CZECHIA":
                    infile.write("reward: " + str(reward) + CURRENCY + "\n\n")
                else:
                    infile.write("reward: " + str(reward) + CURRENCY + "(" + \
                                 str( round(reward/EXCHANGE_RATE)) + "CZK)" "\n\n")
                infile.write(charity + ": " + str(donation) + CURRENCY + "\n\n")
                infile.write("dice: " + str(dice) + CURRENCY + "\n")
                infile.write("lottery: " + str(lottery) + CURRENCY + "\n")
                infile.write("bonus: " + str(bonus) + CURRENCY)
            self.file.write("Winnings\n")
            self.file.write(self.id + "\t" + str(reward) + "\t" + charity + "\t" + str(donation) + "\n\n")
        

    def write(self):
        self.root.texts ["gender"] = self.sex.get()
        self.file.write("Demographics\n")
        self.file.write("\t".join([self.id, self.sex.get(), self.age.get(), self.nationality.get(),
                                   self.language.get(), self.education.get(), self.field.get(),
                                   self.experience.get(), self.position.get()]) + "\n")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Demographics])
