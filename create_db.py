import pandas as pd
from sqlalchemy import create_engine,insert
from sqlalchemy import MetaData,Table, Column, Integer, String, MetaData,Float, Boolean
from sqlalchemy_utils import database_exists, create_database



# On établit une connexion
db_url = "sqlite:///bdd_restaurant.db"
engine = create_engine(db_url)

if not database_exists(engine.url):
    create_database(engine.url)

connection = engine.connect()
trans = connection.begin()

metadata = MetaData(bind=engine)

## Table carte
carte_table = Table('Pays', metadata,
              Column('pays', String(64),primary_key=True)
              )



# Création des tables
metadata.create_all(engine)

trans.commit()
connection.close()