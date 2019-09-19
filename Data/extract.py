import os

studies = ["Identificator",
           "Choice blindness",
           "Choice blindness second part",
           "IAT1",
           "IAT2",
           "IAT3",
           "IAT4",
           "IAT5",
           "IAT6",
           "IAT7",
           "Character",
           "MFQ importance",
           "MFQ attitude",
           "Products",
           "Debriefing",
           "Debriefing2",
           "Demographics",
           "Comments"
           ]


columns = {"Identificator": ("id", "number"),
           "Choice blindness": ("id", "trial", "item", "item_num", "type", "answer", "time"), 
           "Choice blindness second part": ("id", "trial", "item", "item_num", "type", "manipulation",
                                            "answer", "comparison", "changed", "time"),
           "IAT1": ("id", "part", "trial", "item", "answer", "time", "left", "right", "correct"),
           "IAT2": ("id", "part", "trial", "item", "answer", "time", "left", "right", "correct"),
           "IAT3": ("id", "part", "trial", "item", "answer", "time", "left", "right", "correct"),
           "IAT4": ("id", "part", "trial", "item", "answer", "time", "left", "right",
                    "left2", "right2", "correct"),
           "IAT5": ("id", "part", "trial", "item", "answer", "time", "left", "right", "correct"),
           "IAT6": ("id", "part", "trial", "item", "answer", "time", "left", "right",
                    "left2", "right2", "correct"),
           "IAT7": ("id", "part", "trial", "item", "answer", "time", "left", "right",
                    "left2", "right2", "correct"),
           "Character": ("id", "behavior", "person", "condition",
                         "item1", "item2", "item3", "item4", "immoral", "time"),
           "MFQ importance": ("id", "item", "answer"),
           "MFQ attitude": ("id", "item", "answer"),
           "Products": ("id", "trial", "chosen", "chosen_num", "left", "right", "time"),
           "Debriefing": ("id", "attention", "unexpected", "comment"),
           "Debriefing2": ("id", "blindness", "description", "noticed", "knowledge"),
           "Demographics": ("id", "gender", "age", "language", "hand", "student", "field", "education"),
           "Comments": ("id", "comment") 
           }



for study in studies:
    with open("{} results.txt".format(study), mode = "w") as f:
        f.write("\t".join(columns[study]))

files = os.listdir()
for file in files:
    if ".py" in file or "results" in file or ".txt" not in file:
        continue

    with open(file) as datafile:
        for line in datafile:
            study = line.strip()
            if study in studies:
                with open("{} results.txt".format(study), mode = "a") as results:
                    for line in datafile:
                        content = line.strip()
                        if not content:
                            break
                        else:
                            results.write("\n" + content)
                        
                

    
        
