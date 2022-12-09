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


if not "ingredient_star_dep_par_item" in metadata_silver.tables:  # If table don't exist, Create.
    metadata_silver = MetaData(engine_silver)
    # Create a table with the appropriate Columns
    ingredient_star_dep_par_item=Table("ingredient_star_dep_par_item", metadata_silver,
          Column('id', Integer, primary_key=True, nullable=False),
          Column('date', String),
          Column('pays', String),
          Column('dep', String),
          Column('nom_ingredient',String),
          Column('nb_ingredient',Integer)
          )
    # Implement the creation
    metadata_silver.create_all()

with engine.begin() as con:

    request = con.execute("SELECT pays,code_postal,SUM(Recette.quantite*ItemInTicket.quantite) as nb_utiliser,Ingredient.nom FROM Restaurant\
            JOIN Ticket ON Ticket.id_restaurant= Restaurant.id_restaurant\
            JOIN ItemInTicket ON Ticket.id_ticket=ItemInTicket.link_ticket \
            JOIN  Item ON Item.id_item=ItemInTicket.link_item \
            JOIN Recette ON Item.id_item=Recette.link_item \
            JOIN  Ingredient ON Recette.link_ingredient=Ingredient.id_ingredient \
            GROUP BY pays,code_postal,Ingredient.nom\
            ORDER BY pays,code_postal,nb_utiliser DESC")
    id=0
    for row in request:
        
        with engine_silver.begin() as con_silver:
            
            if row[1] != id:
                ins = ingredient_star_dep_par_item.insert().values(date =date_time_str , pays = row[0],dep=row[1][0:2],nom_ingredient=row[3],nb_ingredient=row[2])

                con_silver.execute(ins)
                id = row[1]


if not "ingredient_star_dep_par_menu" in metadata_silver.tables:  # If table don't exist, Create.
    metadata_silver = MetaData(engine_silver)
    # Create a table with the appropriate Columns
    ingredient_star_dep_par_menu=Table("ingredient_star_dep_par_menu", metadata_silver,
          Column('id', Integer, primary_key=True, nullable=False),
          Column('date', String),
          Column('pays', String),
          Column('dep', String),
          Column('nom_ingredient_plat',String),
          Column('nb_ingredient_plat',Integer),
          Column('nom_ingredient_boisson',String),
          Column('nb_ingredient_boisson',Integer),
          Column('nom_ingredient_dessert',String),
          Column('nb_ingredient_dessert',Integer),
          )
    # Implement the creation
    metadata_silver.create_all()

with engine.begin() as con:

    request = con.execute("""SELECT pays,code_postal,SUM(rec_plat.quantite*MenuInTicket.quantite) as nb_utiliser_plat,ingre_plat.nom as plat,SUM(rec_boisson.quantite*MenuInTicket.quantite) as nb_utiliser_boisson,ingre_boisson.nom as boisson,SUM(rec_dessert.quantite*MenuInTicket.quantite) as nb_utiliser_dessert,ingre_dessert.nom as dessert FROM Restaurant
            JOIN Ticket ON Ticket.id_restaurant= Restaurant.id_restaurant
            JOIN MenuInTicket ON Ticket.id_ticket=MenuInTicket.link_ticket 
            JOIN  Menu ON Menu.id_menu=MenuInTicket.link_menu 
            JOIN  Item as plat ON plat.id_item=Menu.plat 
            JOIN  Item as boisson ON boisson.id_item=Menu.boisson 
            JOIN  Item as dessert ON dessert.id_item=Menu.dessert 
            JOIN Recette as rec_plat ON plat.id_item=rec_plat.link_item 
            JOIN Recette as rec_boisson ON boisson.id_item=rec_boisson.link_item
            JOIN Recette as rec_dessert ON dessert.id_item=rec_dessert.link_item
            JOIN  Ingredient as ingre_plat ON rec_plat.link_ingredient=ingre_plat.id_ingredient 
            JOIN  Ingredient as ingre_boisson ON rec_boisson.link_ingredient=ingre_boisson.id_ingredient 
            JOIN  Ingredient as ingre_dessert ON rec_dessert.link_ingredient=ingre_dessert.id_ingredient 
            GROUP BY pays,code_postal,plat,boisson,dessert
            ORDER BY code_postal,nb_utiliser_plat DESC,nb_utiliser_boisson DESC,nb_utiliser_dessert DESC """)
    id=0
    for row in request:
        with engine_silver.begin() as con_silver:
            
            if row[1] != id:
                ins = ingredient_star_dep_par_menu.insert().values(date =date_time_str , pays = row[0],dep=row[1][0:2],nom_ingredient_plat=row[3],nb_ingredient_plat=row[2],nom_ingredient_boisson=row[5],nb_ingredient_boisson=row[4],nom_ingredient_dessert=row[7],nb_ingredient_dessert=row[6])

                con_silver.execute(ins)
                id = row[1]