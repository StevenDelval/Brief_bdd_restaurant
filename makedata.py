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



for elt in list_ingredient:
    ligne = IngredientTable(nom = elt,prix_ingredient = round(random.uniform(0, 1), 2) )
    session.add(ligne)
    session.commit()


for elt in list_nom_item:
    ligne = ItemTable(

        nom =elt,
        prix_de_vente = round(random.uniform(1, 2), 2),
        prix_de_revient = round(random.uniform(0, 1), 2),
        type_item = correspondance_type(elt)
        )
    
    session.add(ligne)
    session.commit()

list_id_ingredient = engine.connect().execute(select([IngredientTable.id_ingredient])).fetchall()
list_id_item =engine.connect().execute(select([ItemTable.id_item])).fetchall()


for i in range(len(list_id_item)):
    for k in range(random.randint(3,6)):
        ligne = RecetteTable(
            id_item = list_id_item[i],
            id_ingredient = list_id_ingredient[k],
            quantite = random.choice([1,2,3])
        )
    session.add(ligne)
    session.commit()








session.close()