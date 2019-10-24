#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

from hexaco import Hexaco
from intros import Intro, Ending
from demo import Demographics
from cheating import Instructions1, BlockOne, Instructions2, BlockTwo, Instructions3, BlockThree
from cheating import EndCheating
from debriefcheating import DebriefCheating
from debriefing import Debriefing
from lottery import Lottery
from anchoring import AnchoringInstructions1, Comparison1, AnchoringInstructions2, Comparison2


frames = [Intro,
          Instructions1,
          BlockOne,
          Instructions2,
          BlockTwo,
          Instructions3,
          BlockThree,
          EndCheating,
          Lottery,
          AnchoringInstructions1,
          Comparison1,
          AnchoringInstructions2,
          Comparison2,
          QuestInstructions,
          Hexaco,
          Demographics,
          DebriefCheating,
          Debriefing,
          Ending
         ]

GUI(frames)
