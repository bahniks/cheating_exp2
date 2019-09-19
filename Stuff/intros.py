#! python3

import os

from common import InstructionsFrame
from gui import GUI
from constants import COUNTRY, BONUS, CURRENCY


################################################################################
# TEXTS
intro = """
Welcome to the research study conducted in cooperation with the Faculty of Business Administration at the University of Economics, Prague. The study consists of several different tasks and questionnaires. Below you see a basic outline of the study:

1) Dice rolling task: You will predict whether an odd or even number will be rolled on a die. You will make predictions for 3 sets consisting of 10 trials each. You can earn money in this part.
2) Lottery task: You will choose a lottery. You can earn money depending on the outcome of the chosen lottery.
3) Distribution of money: You will learn how much you have earned in the previous parts and you can decide what to do with your earnings.
4) Questionnaires: You will answer questions about your characteristics and attitudes. There will be items checking whether you pay attention to the questions. If you answer these attention checks correctly, you can earn additional money.
5) End of the study and payment: After you are finished, you can go to the next room where you sign a contract based on which you will receive your earned money into your bank account. Because only the overall sum will be in the contract, nobody will know how much money you earned in different parts of the study or how you decided to distribute it.  

Thank you for turning off your mobile phones completely and please do not communicate with others in any way during the study. In case you communicate with other participants or disturb the study in any other way, you will be asked to leave the laboratory without payment.

In case you have any questions or you encounter any technical difficulties during the task, just raise your hand and silently wait for a research assistant.

Please, do not continue with the study until you are asked to by a research assistant. 
"""

czechending = """
In the dice rolling task, you earned {} {}. From this amount, you decided to donate {} {} to a charity. In the lottery, you earned {} {}. You have{} correctly answered all attention check items and therefore {} an additional {} {}. Therefore, your reward for the study is {} {}. To this amount, we add 15% tax paid from all wages by an employer and round up the final sum to the nearest 100 Kč. On your contract, you will therefore found the amount {} {}. Please write down this amount together with the number of your seat – {} on a piece of paper you find on your desk. 

The results of the experiment will be freely accessible on the CEBEX website soon after the data evaluation and publication of the findings. We kindly ask you not to mention the details of this research to other potential participants, so that their answers and choices are unaffected.
 
Please raise your hand and one of the research assistants will come and terminate the experiment. You may then collect your belongings, the paper with your seat number and reward, and, without disturbing other participants, go to the room next door where you will sign the contract in order to receive your reward.
 
This is the end of the experiment. Thank you for your participation!
 
CEBEX/PLESS labs
""".format("{}", CURRENCY, # cheating
           "{}", CURRENCY, # charity
           "{}", CURRENCY, # lottery
           "{}", # not /  ... atention check
           "{}", # earned / did not earn ... attention check
           BONUS, CURRENCY, # attention check
           "{}", CURRENCY, # celkem pred zaokrouhlenim
           "{}", CURRENCY, # celkem po zaokrouhleni
           "{}") # seat   
  



chinaending = """
In the dice rolling task, you earned {} {}. From this amount, you decided to donate {} {} to a charity. In the lottery, you earned {} {}. You have{} correctly answered all attention check items and therefore {} an additional {} {}. Therefore, your reward for the study is {} {}. Please write down this amount together with the number of your seat – {} on a piece of paper you find on your desk.

The results of the experiment will be freely accessible on the CEBEX website (cebex.org) soon after the data evaluation and publication of the findings. We kindly ask you not to mention the details of this research to other potential participants, so that their answers and choices are unaffected.

Please raise your hand and one of the research assistants will come and terminate the experiment. You may then collect your belongings, the paper with your seat number and the reward, and, without disturbing other participants, go to the front desk where you will receive your reward.

This is the end of the experiment. Thank you for your participation!

Experimental Economics Lab
""".format("{}", CURRENCY, # cheating
           "{}", CURRENCY, # charity
           "{}", CURRENCY, # lottery
           "{}", # not /  ... attention check
           "{}", # earned / did not earn ... attention check
           BONUS, CURRENCY, # attention check
           "{}", CURRENCY, # celkem
           "{}") # seat



################################################################################

if COUNTRY == "CZECHIA":
    endingtext = czechending
    updates = ["dice", "donation", "lottery_win", "attention1", "attention2", "reward", "rounded_reward", "station"]
else:
    endingtext = chinaending
    updates = ["dice", "donation", "lottery_win", "attention1", "attention2", "reward", "station"]


Intro = (InstructionsFrame, {"text": intro, "keys": ["g", "G"], "proceed": False, "height": 28})
Ending = (InstructionsFrame, {"text": endingtext, "keys": ["g", "G"], "proceed": False, "height": 30,
                              "update": updates})



if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Intro,
         Ending])
