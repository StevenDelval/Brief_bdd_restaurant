from sqlalchemy import create_engine,select
from sqlalchemy import MetaData,Table, Column, Integer, String, MetaData,Float,Boolean, CheckConstraint,ForeignKey
from sqlalchemy.orm import sessionmaker 
from sqlalchemy_utils import database_exists, create_database
from create_db import CarteTable,RestaurantTable,EmployeTable,SalaireTable,IngredientTable,StockTable,ItemTable,RecetteTable,MenuTable,MenuInCarteTable,ItemInCarteTable,TicketTable,ItemInTicketTable,MenuInTicketTable
from functions import *
from datetime import datetime

db_url = "sqlite:///bdd_restaurant.db"
engine = create_engine(db_url)
Session = sessionmaker(bind=engine) 
session = Session()

db_url_silver = "sqlite:///bdd_restaurant_silver.db"
engine_silver = create_engine(db_url_silver)

if not database_exists(engine_silver.url):
    create_database(engine_silver.url)

Session_silver = sessionmaker(bind=engine_silver) 
session_silver = Session()

metadata_silver = MetaData(engine_silver)
if not "employe_dep" in metadata_silver.tables:  # If table don't exist, Create.
    metadata_silver = MetaData(engine_silver)
    # Create a table with the appropriate Columns
    employe_dep=Table("employe_dep", metadata_silver,
          Column('id', Integer, primary_key=True, nullable=False),
          Column('date', String),
          Column('pays', String),
          Column('dep', String),
          Column('nb_employe',Integer)
          )
    # Implement the creation
    metadata_silver.create_all()

now = datetime.now()
date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

with engine.begin() as con:
    request = con.execute("SELECT pays,code_postal,COUNT(id_employe) FROM Restaurant\
        JOIN Employe ON Employe.id_restaurant= Restaurant.id_restaurant\
            GROUP BY pays,code_postal")
    
    for row in request:
        with engine_silver.begin() as con_silver:
            ins = employe_dep.insert().values(date =date_time_str , pays = row[0],dep=row[1][0:2],nb_employe=row[2])

            con_silver.execute(ins)



    
