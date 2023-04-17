from models.credito import Credito as CreditoModel 
from schemas.credito import Credito

class CrediService():
    
    def __init__(self, db) -> None:
        self.db = db
        
    def get_creditos(self):
        result = self.db.query(CreditoModel).all()
        return result
    
    def get_credito(self, id):
        result = self.db.query(CreditoModel).filter(CreditoModel.id == id).first()
        return result
    
    def create_credito(self, credito:Credito):
        new_credito = CreditoModel(**credito.dict())
        self.db.add(new_credito)
        self.db.commit()
        return
    
    def update_credito(self, id: int, data: Credito):
        credito = self.db.query(CreditoModel).filter(CreditoModel.id == id).first()
        credito.nombre = data.nombre
        credito.estado = data.estado
        credito.ingresos = data.ingresos
        credito.score = data.score
        credito.centralesRiesgo = data.centralesRiesgo
        self.db.commit()
        return
    
    def delete_credito(self, id: int):
        self.db.query(CreditoModel).filter(CreditoModel.id == id).delete()
        self.db.commit()
        return