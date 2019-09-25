#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

from questionnaire import Prosociality, Values1, Values2, Values3
from quest import QuestInstructions, Hexaco
from intros import Intro, Ending
from demo import Demographics
from cheating import Instructions1, BlockOne, Instructions2, BlockTwo, Instructions3, BlockThree
from cheating import EndCheating, DebriefCheating
from debriefing import Debriefing
from lottery import Lottery


frames = [Intro,
          Instructions1,
          BlockOne,
          Instructions2,
          BlockTwo,
          Instructions3,
          BlockThree,
          EndCheating,
          Lottery,
          QuestInstructions,
          Hexaco,
          DebriefCheating,
          Debriefing,
          Ending
         ]

GUI(frames)
