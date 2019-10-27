#! python3

import os

from common import InstructionsFrame
from gui import GUI

from constants import BONUS


################################################################################
# TEXTS
intro = """
Vítejte na výzkumné studii pořádané ve spolupráci s Fakultou podnikohospodářskou Vysoké školy ekonomické v Praze. Tato studie se skládá z několika různých úkolů a otázek. Níže je uveden přehled toho, co vás čeká:

1) Hod kostkou: vaším úkolem bude uhodnout, zda na kostce padne liché nebo sudé číslo. Budete hádat v pěti blocích, každém po dvanácti kolech. V tomto úkolu můžete vydělat peníze.
2) Loterie: budete volit loterii. Můžete vydělat peníze v závislosti na výsledku zvolené loterie.
3) Odhady hodnot: budete odhadovat a porovnávat různé hodnoty týkající se všeobecných znalostí a uvádět příklady různých kategorií.
4) Dotazníky: budete odpovídat na otázky ohledně vašich vlastností a postojů. Dotazník zahrnuje položky, které kontrolují, zda otázkám věnujete pozornost. Pokud odpovíte na tyto kontroly pozornosti správně, získáte další peníze. 
5) Konec studie a platba: poté, co skončíte, půjdete do vedlejší místnosti, kde podepíšete pokladní dokument, na základě kterého obdržíte vydělané peníze v hotovosti. Jelikož v dokumentu bude uvedena pouze celková suma, nikdo se nedoví, kolik jste vydělali v jednotlivých částech studie.

Děkujeme, že jste vypnuli své mobilní telefony, a že nebudete s nikým komunikovat v průběhu studie. Pokud s někým budete komunikovat, nebo pokud budete nějakým jiným způsobem narušovat průběh studie, budete požádáni, abyste opustili laboratoř, bez nároku na vyplacení peněz.

V případě, že máte otázky nebo narazíte na technický problém během úkolů, zvedněte ruku a tiše vyčkejte příchodu výzkumného asistenta.

Nepokračujte prosím dokud vám výzkumný asistent nedá pokyn.
"""


czechending = """
V úkolu s kostkou jste vydělali {} Kč. V loterii jste vydělali {} Kč. {} jste správně na všechny kontroly pozornosti a tedy {} dalších {} Kč. Vaše odměna za tuto studii je tedy {} Kč, zaokrouhleno na desítky nahoru {} Kč. Napište prosím tuto (zaokrouhlenou) částku společně s číslem vašeho místa – {} na papír na vašem stole před vámi. 

Výsledky experimentu budou volně dostupné na stránkách PLESS a CEBEX, krátce po vyhodnocení dat a publikaci výsledků. Žádáme vás, abyste nesdělovali detaily tohoto výzkumu možným účastníkům, aby jejich volby a odpovědi nebyly ovlivněny a znehodnoceny.
  
Zvedněte prosím ruku a některý z výzkumných asistentů přijde a ukončí experiment. Poté si můžete vzít všechny svoje věci, papír s číslem vašeho místa a uvedenou odměnou, a bez toho, aniž byste rušili ostatní účastníky, se odeberte do vedlejší místnosti, kde obdržíte svoji odměnu. 

Toto je konec experimentu. Děkujeme za vaši účast!
 
CEBEX/PLESS labs
""" 






################################################################################


updates = ["dice", "lottery_win", "attention1", "attention2", BONUS, "reward", "rounded_reward", "station"]



Intro = (InstructionsFrame, {"text": intro, "keys": ["g", "G"], "proceed": False, "height": 28})
Ending = (InstructionsFrame, {"text": czechending, "keys": ["g", "G"], "proceed": False, "height": 30,
                              "update": updates})



if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Intro,
         Ending])
