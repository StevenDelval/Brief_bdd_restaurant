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


list_burger = ['Le Tomme des Pyrénées IGP & Bacon Fumé - 1 viande','Le Tomme des Pyrénées IGP & Bacon Fumé - 2 viandes','Le Beef BBQ - 1 viande','Le Beef BBQ - 2 Viandes','Le Big Mac','Le McChicken','Le 280 Original','Le Filet-O-Fish','Le Double Filet-O-fish','Le Cheeseburger','Le Cheeseburger Bacon','Le Triple Cheeseburger Bacon']

list_boisson=['coca33ml','coca50ml','coca100ml','le nectar de pomme bio','minute maid orange']

list_salade =['Italian Mozza & Pasta','La Tasty Blue Cheese & Bacon','La Classic Caesar']

list_dessert = ['le mcflurry','le sundea','le petit glace saveur vanille','le donut nature','le duo de macarons']

list_menu = ['Le Menu Best Of','Le Menu Maxi Best Of','Le Menu Salade']


list_nom_item = list_burger + list_boisson + list_salade + list_dessert

def correspondance_type(elt):
    if elt in list_burger:
        return 'buger'
    elif elt in list_boisson:
        return 'boisson'
    elif elt in list_salade:
        return 'salade'
    elif elt in list_dessert:
        return 'dessert'
    

