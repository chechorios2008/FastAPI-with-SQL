from config.database import Base
from sqlalchemy import Column, Integer, String, Float

class Credito(Base):
    
    __tablename__ = "credito"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    estado = Column(String)
    ingresos = Column(Integer)
    score = Column(Float)
    centralesRiesgo = Column(String)
    
    
