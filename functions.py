import os
from math import ceil
import random

random.seed(0)

def loading(percent):
    """
    Fonction qui nettoye le terminal.
    """
    my_os = os.name
    if my_os == "posix":
        os.system('clear')
    else:
        os.system('cls')
    print('[ ' + '#'*ceil(20*(percent)/100) + ' '*ceil(20*(100-percent)/100) + ' ]')


def correspondance(pays_code):
    if pays_code == "fr_FR":
        return "France"
    if pays_code == "en_US":
        return "Etat Unie"
    if pays_code == "es_ES":
        return "Espagne"
    if pays_code == "it_IT":
        return "Italie"
    if pays_code == "ja_JP":
        return "Japon"
    if pays_code == "en_GB":
        return "Grande Bretagne"

def inv_correspondance(pays):
    if pays == "France":
        return "fr_FR"
    if pays == "Etat Unie":
        return "en_US"
    if pays == "Espagne":
        return "es_ES"
    if pays == "Italie":
        return "it_IT"
    if pays == "Japon":
        return "ja_JP"
    if pays == "Grande Bretagne":
        return "en_GB"

def salaire_poste(poste):
    if poste == "directeur":
        return random.uniform(4000,5000)
    if poste == "manager":
        return random.uniform(2000,4000)
    if poste == "caissiers":
        return random.uniform(1000,1800)
    if poste == "cuisiniers":
        return random.uniform(1200,2000)
    

