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

faker_arg = ["fr_FR", "en_US","es_ES","it_IT","ja_JP","en_GB"]
for country in faker_arg:
    ligne = CarteTable(pays = correspondance(country))
    session.add(ligne)
    session.commit()

for arg in faker_arg:
    fake = Faker(arg)
    for nb in range(random.randint(1,60)):
        ligne=RestaurantTable(pays=correspondance(arg),ville=fake.city(),\
            code_postal=fake.postcode(),capacite=random.randint(40,200),\
            espace_enfant=random.randint(0,1),borne_service=random.randint(0,1),\
            accessible_pmr=random.randint(0,1),parking=random.randint(0,1)
            )
        session.add(ligne)
        session.commit()

list_ingredient =['Bœuf', 'poulet', 'pomme de terre', 'blé', 'salade', 'poisson', 'oeuf', 'pommes','coca33ml','coca50ml','coca100ml','le nectar de pomme bio','minute maid orange','le mcflurry','le sundea','le petit glace saveur vanille','le donut nature','le duo de macarons']

for elt in list_ingredient:
    ligne = IngredientTable(nom = elt,prix_ingredient = round(random.uniform(0, 1), 2) )
    session.add(ligne)
    session.commit()

list_nom_item =
ligne = ItemTable(
    nom = ,
    prix_de_vente = ,
    prix_de_revient =,
    type_item = ,
)




session.close()