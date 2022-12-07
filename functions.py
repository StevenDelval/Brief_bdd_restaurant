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
