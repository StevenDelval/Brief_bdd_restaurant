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
faker_arg = ["fr_FR", "en_US","es_ES","it_IT","ja_JP","en_GB"]
for country in faker_arg:
    ligne = CarteTable(pays = correspondance(country))
    session.add(ligne)
    session.commit()

## Remplire table restaurant
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

## Remplire table employe
for restaurant in session.query(RestaurantTable).all():
    fake = Faker(inv_correspondance(restaurant.pays))
    
    #### Creation directeur pour le restaurant
    ligne= EmployeTable(id_restaurant=restaurant.id_restaurant,\
        nom=fake.last_name(),prenom=fake.first_name(),\
        adresse=fake.street_address(),experience=random.randint(0,30),\
        poste="directeur",note=random.randint(8,10),date_entree=str(fake.date_object()))
    session.add(ligne)
    session.commit()
    id_directeur = session.query(EmployeTable).all()[-1].id_employe

    
    #### Creation des manager pour le directeur
    for manager in range(random.randint(0,5)):
        ligne= EmployeTable(id_superviseur=id_directeur,id_restaurant=restaurant.id_restaurant,\
            nom=fake.last_name(),prenom=fake.first_name(),\
            adresse=fake.street_address(),experience=random.randint(0,30),\
            poste="manager",note=random.randint(1,10),date_entree=str(fake.date_object()))
        session.add(ligne)
        session.commit()
        id_manager = session.query(EmployeTable).all()[-1].id_employe
        
        
    #### Creation des employe pour le manager
        for employe in range(random.randint(0,10)):
            poste = random.choice(["caissiers","cuisiniers"])
            ligne= EmployeTable(id_superviseur=id_manager,id_restaurant=restaurant.id_restaurant,\
                nom=fake.last_name(),prenom=fake.first_name(),\
                adresse=fake.street_address(),experience=random.randint(0,30),\
                poste=poste,note=random.randint(1,10),date_entree=str(fake.date_object()))
            session.add(ligne)
            session.commit()

## Remplire table salaire
for employe in session.query(EmployeTable).all() :
    ligne = SalaireTable(id_employe=employe.id_employe,salaire=random.uniform(1200,5000),data_de_paie="2022-11-30")
    session.add(ligne)
    session.commit()
    




session.close()