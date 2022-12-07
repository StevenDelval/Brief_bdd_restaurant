from sqlalchemy import create_engine
from sqlalchemy import MetaData,Table, Column, Integer, String, MetaData,Float,Boolean, CheckConstraint,ForeignKey
from sqlalchemy.orm import sessionmaker 
from faker import Faker
from create_db import *
from functions import *
import random

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




session.close()