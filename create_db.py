import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import MetaData,Table, Column, Integer, String, MetaData,Float,Boolean, CheckConstraint,ForeignKey
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,column_property



# On établit une connexion
db_url = "sqlite:///bdd_restaurant.db"
engine = create_engine(db_url)

if not database_exists(engine.url):
    create_database(engine.url)

Session = sessionmaker(bind=engine) 

session = Session()

Base = declarative_base()




## Table carte
class CarteTable(Base):
    __tablename__ = 'Carte'
    
    pays = Column('pays', String(64),primary_key=True)

## Table restaurant
class RestaurantTable(Base):
    __tablename__ = 'Restaurant'
    id_restaurant = Column('id_restaurant', Integer(),primary_key=True)
    pays = Column('pays',Integer(),ForeignKey('Carte.pays'))
    ville = Column('ville',String(128))
    code_postal = Column('code_postal',String(5))
    capacite = Column('capacite',Integer())
    espace_enfant = Column('espace_enfant',Integer())
    borne_service = Column('borne_service',Integer())
    accessible_pmr = Column('accessible_pmr',Integer())
    parking = Column('parking',Integer())
    
    def liste_tous_resto():
        """
        Methode qui liste tous les restaurants
        :return list
        """
        return session.query(RestaurantTable).all()

## Table employe
class EmployeTable(Base):
    __tablename__ ='Employe'
    id_employe = Column('id_employe',Integer(), primary_key = True)
    id_superviseur = Column('id_superviseur', Integer(),ForeignKey('Employe.id_employe'))
    id_restaurant = Column('id_restaurant',Integer(),ForeignKey('Restaurant.id_restaurant'))
    nom = Column('nom',String())
    prenom = Column('prenom',String())
    adresse = Column('adresse',String())
    experience = Column('experience', Integer())
    poste = Column('poste',String())
    note = Column('note',Integer())
    date_entree = Column('date_entree',String())
    
    def tous_les_employe():
        """
        Methode qui liste tous les employees
        :return list object
        """
        return session.query(EmployeTable).all()
    def dernier_employe():
        """
        Methode qui donne le dernier employe ajoute
        :return id_employe
        """
        return session.query(EmployeTable).all()[-1].id_employe
    def poste_employe(id):
        """
        Methode qui donne le poste de l'employe 
        :return poste 
        """
        return session.query(EmployeTable).filter_by(id_employe=id).first().poste

## Table salaire
class SalaireTable(Base):
    __tablename__ = 'Salaire'
    id_paie = Column('id_paie',Integer(),primary_key = True)
    id_employe = Column('id_employe',Integer(),ForeignKey('Employe.id_employe'))
    salaire = Column('salaire',Float(precision = 2))
    data_de_paie = Column('date_de_paie',String())

## Table ingredient
class IngredientTable(Base):
    __tablename__ = 'Ingredient'
    id_ingredient =Column('id_ingredient',Integer(),primary_key =True)
    nom = Column('nom',String())
    prix_ingredient = Column('prix_ingredient',Float(precision = 2))

    def liste_ingredient():
        """
        Methode qui liste tous les Ingredients
        :return list
        """
        return session.query(IngredientTable).all()

## Table stock
class StockTable(Base):
    __tablename__ = 'Stock'
    id_restaurant = Column('id_restaurant',Integer(), ForeignKey('Restaurant.id_restaurant'),primary_key = True)
    id_ingredient = Column('id_ingredient',Integer(),ForeignKey('Ingredient.id_ingredient'),primary_key = True)
    nombre = Column('nombre',Integer())

## Table item
class ItemTable(Base):
    __tablename__ = 'Item'
    id_item = Column('id_item',Integer(),primary_key = True)
    nom = Column('nom',String())
    prix_de_vente = Column('prix_de_vente',Float(precision=2))
    prix_de_fabrication =Column('prix_de_fabrication',Float(precision=2))
    type_item = Column('type_item',String())
    def liste_item():
        return session.query(ItemTable).all() 

## Table recette
class RecetteTable(Base):
    __tablename__ = 'Recette'
    link_item = column_property(Column(Integer,primary_key = True), ItemTable.id_item)
    link_ingredient = column_property(Column(Integer,primary_key = True), IngredientTable.id_ingredient)
    id_item = Column(Integer(),ForeignKey('Item.id_item'))
    id_ingredient = Column(Integer(),ForeignKey('Ingredient.id_ingredient'))
    quantite = Column('quantite',Integer())

## Table menu
class MenuTable(Base):
    __tablename__ = 'Menu'
    id_menu =Column('id_menu',Integer(),primary_key = True)
    prix_de_vente = Column('prix_de_vente',Float(precision=2))
    nom = Column('nom',String())
    plat = Column('plat',Integer(),ForeignKey('Item.id_item'))
    dessert = Column('dessert',Integer(),ForeignKey('Item.id_item'))
    boisson = Column('boisson',Integer(),ForeignKey('Item.id_item'))

## Table  menu in carte
class MenuInCarteTable(Base):
    __tablename__ = 'MenuInCarte'
    link_menu = column_property(Column(Integer(),primary_key = True), MenuTable.id_menu)
    link_pays = column_property(Column(Integer(),primary_key = True), CarteTable.pays)
    pays = Column('pays',Integer(),ForeignKey('Carte.pays'),primary_key = True)
    id_menu =Column('id_menu',Integer(),ForeignKey('Menu.id_menu'),primary_key = True)

## Table item in carte
class ItemInCarteTable(Base):
    __tablename__ = 'ItemInCarte'
    link_item = column_property(Column(Integer(),primary_key = True), ItemTable.id_item)
    link_pays = column_property(Column(Integer(),primary_key = True), CarteTable.pays)
    pays = Column('pays',Integer(),ForeignKey('Carte.pays'),primary_key = True)
    id_item =Column('id_item',Integer(),ForeignKey('Item.id_item'),primary_key = True)

## Table ticket
class TicketTable(Base):
    __tablename__ ='Ticket'
    id_ticket = Column('id_ticket', Integer(),primary_key = True)
    id_restaurant = Column('id_restaurant', Integer(),ForeignKey('Restaurant.id_restaurant'))
    id_employe = Column('id_employe',Integer(), ForeignKey('Employe.id_employe'))
    borne = Column('borne',Integer())
    heure =Column('heure',String())
    moyen_de_payment = Column('moyen_de_payment',String())
    prix_total = Column('prix_total',Float(precision=2))

## Table item in ticket
class ItemInTicketTable(Base):
    __tablename__ = 'ItemInTicket'
    link_ticket = column_property(Column(Integer(),primary_key = True), TicketTable.id_ticket)
    link_item = column_property(Column(Integer(),primary_key = True), ItemTable.id_item)
    id_ticket = Column('id_ticket', Integer(),ForeignKey('Ticket.id_ticket'),primary_key = True)
    id_item =Column('id_item',Integer(),ForeignKey('Item.id_item'),primary_key = True)



## Table menu in ticket
class MenuInTicketTable(Base):
    __tablename__ = 'MenuInTicket'
    link_menu = column_property(Column(Integer(),primary_key = True), MenuTable.id_menu)
    link_ticket = column_property(Column(Integer(),primary_key = True), TicketTable.id_ticket)
    id_ticket = Column('id_ticket', Integer(),ForeignKey('Ticket.id_ticket'),primary_key = True)
    id_menu =Column('id_menu',Integer(),ForeignKey('Menu.id_menu'),primary_key = True)
    


# Création des tables

Base.metadata.create_all(bind=engine)

session.close()