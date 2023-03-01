import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base #Para manipulas las tablas de la BD.

sqlite_file_name = "../database.sqlite"
base_dir = os.path.dirname(os.path.realpath(__file__)) #Lee el directorio Path. 

database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}" #URL de la BD.

engine = create_engine(database_url, echo=True) #Eco; muestra por consola lo que se esta haciendo. 

Session = sessionmaker(bind=engine)

Base = declarative_base()