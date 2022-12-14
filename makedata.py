from sqlalchemy import create_engine,select
from sqlalchemy import MetaData,Table, Column, Integer, String, MetaData,Float,Boolean, CheckConstraint,ForeignKey
from sqlalchemy.orm import sessionmaker 
from faker import Faker
from create_db import *
from functions import *
import random

random.seed(0)
Faker.seed(0)

db_url = "sqlite:///bdd_restaurant.db"
engine = create_engine(db_url)
Session = sessionmaker(bind=engine) 
session = Session()

## Remplire table carte
faker_arg = ["fr_FR" , "en_US","es_ES","it_IT","ja_JP","en_GB"]
for country in faker_arg:
    loading(0)
    
    ligne = CarteTable(pays = correspondance(country))
    loading(50)

    session.add(ligne)
    session.commit()
    loading(100)

## Remplire table restaurant
for arg in faker_arg:
    
    fake = Faker(arg)
    
    for nb in range(random.randint(1,20)):
        loading(0)

        ligne=RestaurantTable(pays=correspondance(arg),ville=fake.city(),\
            code_postal=fake.postcode(),capacite=random.randint(40,200),\
            espace_enfant=random.randint(0,1),borne_service=random.randint(0,1),\
            accessible_pmr=random.randint(0,1),parking=random.randint(0,1)
            )
        
        loading(50)
        
        session.add(ligne)
        session.commit()

        loading(100)

## Remplire table employe
for restaurant in RestaurantTable.liste_tous_resto():
    fake = Faker(inv_correspondance(restaurant.pays))
    
    loading(0)
    #### Creation directeur pour le restaurant
    ligne= EmployeTable(id_restaurant=restaurant.id_restaurant,\
        nom=fake.last_name(),prenom=fake.first_name(),\
        adresse=fake.street_address(),experience=random.randint(0,30),\
        poste="directeur",note=random.randint(8,10),date_entree=str(fake.date_object()))
    
    loading(50)
    
    session.add(ligne)
    session.commit()
    id_directeur = EmployeTable.dernier_employe()
    
    loading(100)
    
    #### Creation des manager pour le directeur
    for manager in range(random.randint(1,4)):
        
        loading(0)
        
        ligne= EmployeTable(id_superviseur=id_directeur,id_restaurant=restaurant.id_restaurant,\
            nom=fake.last_name(),prenom=fake.first_name(),\
            adresse=fake.street_address(),experience=random.randint(0,30),\
            poste="manager",note=random.randint(1,10),date_entree=str(fake.date_object()))
        
        loading(50)
        
        session.add(ligne)
        session.commit()
        id_manager = EmployeTable.dernier_employe()
        
        loading(100)
        
    #### Creation des employe pour le manager
        for employe in range(random.randint(1,4)):
            
            loading(0)
            
            poste = random.choice(["caissiers","cuisiniers"])
            ligne= EmployeTable(id_superviseur=id_manager,id_restaurant=restaurant.id_restaurant,\
                nom=fake.last_name(),prenom=fake.first_name(),\
                adresse=fake.street_address(),experience=random.randint(0,30),\
                poste=poste,note=random.randint(1,10),date_entree=str(fake.date_object()))
            
            loading(50)
            
            session.add(ligne)
            session.commit()
            
            loading(100)

## Remplire table salaire
for employe in EmployeTable.tous_les_employe() :

    loading(0)
    
    poste = EmployeTable.poste_employe(employe.id_employe)
    
    ligne = SalaireTable(id_employe=employe.id_employe,salaire=salaire_poste(poste),data_de_paie="2022-11-30")
    
    loading(50)
    
    session.add(ligne)
    session.commit()
    
    loading(100)

## Remplire table ingredient
list_ingredient =['boeuf','pain',"steak", 'poulet','maroille',"eau" ,'pomme de terre', 'bl??', 'salade', 'poisson', 'oeuf',"poire", 'pommes','coca33ml','coca50ml','coca100ml','fanta33ml','fanta50ml','fanta100ml']

for elt in list_ingredient:
    loading(0)

    ligne = IngredientTable(nom = elt,prix_ingredient = round(random.uniform(0, 1), 2) )
    
    loading(50)
    
    session.add(ligne)
    session.commit()
    
    loading(100)

## Remplire table stock
for restaurant in RestaurantTable.liste_tous_resto():
    for ingredient in IngredientTable.liste_ingredient():
         
        loading(0)

        ligne = StockTable(id_restaurant=restaurant.id_restaurant,\
            id_ingredient=ingredient.id_ingredient,nombre=random.randint(100,10000))

    
        loading(50)
    
        session.add(ligne)
        session.commit()
    
    
        loading(100)

## Remplire table item
list_burger = ['Le Tomme des Pyr??n??es IGP & Bacon Fum?? - 1 viande','Le Tomme des Pyr??n??es IGP & Bacon Fum?? - 2 viandes','Le Beef BBQ - 1 viande','Le Beef BBQ - 2 Viandes','Le Big Mac','Le McChicken','Le 280 Original','Le Filet-O-Fish','Le Double Filet-O-fish','Le Cheeseburger','Le Cheeseburger Bacon','Le Triple Cheeseburger Bacon']
list_boisson=['coca33ml','coca50ml','coca100ml','le nectar de pomme bio','minute maid orange']
list_dessert = ['le mcflurry','le sundea','le petit glace saveur vanille','le donut nature','le duo de macarons']

for plat in list_burger :
    loading(0)

    
    ligne = ItemTable(nom=plat,type_item="plat")
    
    loading(50)
    
    session.add(ligne)
    session.commit()
    
    loading(100)  
for plat in list_boisson :
    loading(0)

    
    ligne = ItemTable(nom=plat,type_item="boisson")
    
    loading(50)
    
    session.add(ligne)
    session.commit()
    
    loading(100)  
for plat in list_dessert :
    loading(0)

    
    ligne = ItemTable(nom=plat,type_item="dessert")
    
    loading(50)
    
    session.add(ligne)
    session.commit()
    
    loading(100)  

## Remplire Recette
list_ingredient = IngredientTable.liste_ingredient()
list_item = ItemTable.liste_item()

for item in list_item:

    nb_ingredient=random.randint(3,6)
    liste_choix=random.sample(list_ingredient,nb_ingredient)

    for k in range(nb_ingredient):
        loading(0)

        ligne = RecetteTable(\
            link_item = item.id_item,\
            link_ingredient = liste_choix[k].id_ingredient,\
            quantite = random.choice([1,2,3])\
        )
        loading(50)

        session.add(ligne)
        session.commit()

        loading(100)

## Correction prix des Item
list_item = ItemTable.liste_item()
for item in list_item :
    loading(0)
    with engine.begin() as con:
        rs = con.execute("Select Item.id_item,SUM( Recette.quantite * Ingredient.prix_ingredient)  FROM Item \
                JOIN Recette ON Item.id_item=Recette.link_item \
                JOIN  Ingredient ON Recette.link_ingredient=Ingredient.id_ingredient \
                WHERE Item.id_item = (?) \
                GROUP BY Item.id_item ",(item.id_item))
        loading(50)
        for row in rs:
        
            con.execute("Update Item SET prix_de_fabrication = ? ,prix_de_vente = ? WHERE id_item = ? ",(round(row[1],2),round(row[1]+2,2),item.id_item))
            
session.close_all()
db_url = "sqlite:///bdd_restaurant.db"
engine = create_engine(db_url)
Session = sessionmaker(bind=engine) 
session = Session()

## Remplire Menu
for nb in range(random.randint(5,30)) :
    fake = Faker("fr_FR")
    loading(0)
    
    plat =random.choice(ItemTable.select_type("plat"))
    boisson =random.choice(ItemTable.select_type("boisson"))
    dessert =random.choice(ItemTable.select_type("dessert"))
    text = fake.text().split(' ')
    nom_menu = text[0] + text [1] + text[2] 
    
    ligne = MenuTable(nom=nom_menu,plat=plat.id_item,boisson=boisson.id_item,dessert = dessert.id_item ,\
        prix_de_vente=round((plat.prix_de_vente + boisson.prix_de_vente + dessert.prix_de_vente)-1,2)) 
    
    loading(50)
    
    session.add(ligne)
    session.commit()
    
    loading(100)

## Creation ticket
for restaurant in RestaurantTable.liste_tous_resto():
    for nb in range(random.randint(5,20)):
        employe =random.choice(EmployeTable.employe_restaurant(restaurant.id_restaurant))
        borne = 0
        if EmployeTable.poste_employe(employe.id_employe) == "directeur":
            borne = 1

        loading(0)
        minute =random.randint(0,59)
        if minute < 10:
            minute = "0"+ str(minute)
        else:
            minute= str(minute)
        ligne = TicketTable(id_restaurant=restaurant.id_restaurant,\
            id_employe=employe.id_employe,borne=borne,heure=(str(random.randint(8,23))+":"+minute),\
                moyen_de_payment=random.choice(['cb','espece'])) 
    
        loading(50)
    
        session.add(ligne)
        session.commit()
    
        loading(100)

## Remplir menu in carte
liste_carte = CarteTable.liste_carte()
liste_menu = MenuTable.liste_menu()

for carte in liste_carte:

    nb_menu=random.randint(2,len(liste_menu))
    liste_choix=random.sample(liste_menu,nb_menu)

    for k in range(nb_menu):
        loading(0)

        ligne = MenuInCarteTable(\
            link_menu = liste_choix[k].id_menu,\
            link_pays = carte.pays)
        
    
        loading(50)

        session.add(ligne)
        session.commit()

        loading(100)
## Remplir item in carte
liste_carte = CarteTable.liste_carte()
liste_item = ItemTable.liste_item()

for carte in liste_carte:

    nb_item=random.randint(2,len(liste_item))
    liste_choix=random.sample(liste_item,nb_item)

    for k in range(nb_item):
        loading(0)

        ligne = ItemInCarteTable(\
            link_item = liste_choix[k].id_item,\
            link_pays = carte.pays)
        
    
        loading(50)

        session.add(ligne)
        session.commit()

        loading(100)


## Remplire Menu in ticket
liste_ticket = TicketTable.liste_ticket()

for ticket in liste_ticket:
    id_restaurant = ticket.id_restaurant
    pays_restaurant =RestaurantTable.pays_restaurant(id_restaurant)
    liste_menu_carte =MenuInCarteTable.menu_pays(pays_restaurant)
    


    nb_menu=random.randint(1,len(liste_menu_carte))
    liste_choix=random.sample(liste_menu_carte,nb_menu)

    for k in range(nb_menu):
        loading(0)
        
        ligne = MenuInTicketTable(\
            link_menu = liste_choix[k].link_menu,\
            link_ticket = ticket.id_ticket,quantite = random.choice([1,2,3]))
        
    
        loading(50)

        session.add(ligne)
        session.commit()

        loading(100)

## Remplire item in ticket
for ticket in liste_ticket:
    id_restaurant = ticket.id_restaurant
    pays_restaurant =RestaurantTable.pays_restaurant(id_restaurant)
    liste_item_carte =ItemInCarteTable.item_pays(pays_restaurant)


    nb_menu=random.randint(1,len(liste_item_carte))
    liste_choix=random.sample(liste_item_carte,nb_menu)

    for k in range(nb_menu):
        loading(0)

        ligne = ItemInTicketTable(\
            link_item = liste_choix[k].link_item,\
            link_ticket = ticket.id_ticket,quantite = random.choice([1,2,3]))
        
    
        loading(50)

        session.add(ligne)
        session.commit()

        loading(100)



session.close_all()

db_url = "sqlite:///bdd_restaurant.db"
engine = create_engine(db_url)
Session = sessionmaker(bind=engine) 
session = Session()
liste_ticket = TicketTable.liste_ticket()

for ticket in liste_ticket:
    loading(0)
    with engine.begin() as con:
        item = con.execute("Select Ticket.id_ticket,SUM( ItemInTicket.quantite * Item.prix_de_vente)  FROM Ticket \
                JOIN ItemInTicket ON Ticket.id_ticket=ItemInTicket.link_ticket \
                JOIN  Item ON Item.id_item=ItemInTicket.link_item \
                WHERE Ticket.id_ticket = (?) \
                GROUP BY Ticket.id_ticket ",(ticket.id_ticket))
        loading(50)
        for row in item:
            total_item =round(row[1],2)

        menu = con.execute("Select Ticket.id_ticket,SUM( MenuInTicket.quantite * Menu.prix_de_vente)  FROM Ticket \
                JOIN MenuInTicket ON Ticket.id_ticket=MenuInTicket.link_ticket \
                JOIN  Menu ON Menu.id_menu=MenuInTicket.link_menu \
                WHERE Ticket.id_ticket = (?) \
                GROUP BY Ticket.id_ticket ",(ticket.id_ticket))
        for row in menu:
            total_menu =round(row[1],2)
        total =round(total_item + total_menu,2)
        con.execute("Update Ticket SET prix_total = ? WHERE id_ticket = ? ",(total,ticket.id_ticket))
        loading(100)