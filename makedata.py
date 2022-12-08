from sqlalchemy import create_engine
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
faker_arg = ["fr_FR"] # , "en_US","es_ES","it_IT","ja_JP","en_GB"]
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
    
    for nb in range(random.randint(1,60)):
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
    for manager in range(random.randint(0,5)):
        
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
        for employe in range(random.randint(0,10)):
            
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
list_ingredient =['boeuf','pain',"steak", 'poulet','maroille',"eau" ,'pomme de terre', 'blé', 'salade', 'poisson', 'oeuf',"poire", 'pommes','coca33ml','coca50ml','coca100ml','fanta33ml','fanta50ml','fanta100ml']

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



session.close()