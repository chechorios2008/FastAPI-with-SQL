from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.credito import Credito as CreditModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.credito import CrediService
from schemas.credito import Credito

movie_router = APIRouter()

@movie_router.get(
    path='/credits',
    tags=['Credit'],
    summary="Show all credits",
    response_model=List[Credito],
    status_code=200,
    dependencies= [Depends(JWTBearer())])
def get_movies() -> List[Credito]:
    db = Session()
    result = CrediService(db).get_creditos()
    return JSONResponse(status_code=200, content=jsonable_encoder(result)) 

@movie_router.get('/credits/{id}', 
    tags=['Credit'],
    summary="Obtener crédito por ID",
    response_model=Credito,
    status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Credito:
    db = Session()
    result = CrediService(db).get_credito(id)
    if not result:
        return JSONResponse(status_code=404, content={'message':'Cliente no registrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post(
    path='/credits',
    tags=['Credit'],
    summary="Crear a registro de crédito.",
    response_model=dict,
    status_code=201)
def create_movie(credit: Credito) -> dict:
    db = Session()
    CrediService(db).create_credito(credit)
    return JSONResponse(status_code=201,content={"message":"Tú crédito ha sido registrado con éxito"})

@movie_router.put(
    path='/credits/{id}',
    tags=['Credit'],
    summary="Modificar crédito",
    response_model=dict,
    status_code=200)
def update_movies(id:int, credit: Credito) -> dict:
    db = Session()
    result = CrediService(db).get_credito(id)
    if not result:
        return JSONResponse(status_code=404, content={'message':'Cliente no registrado'})
    CrediService(db).update_credito(id, credit)
    return JSONResponse(status_code=200, content={"message":"Crédito actualizado"})            
            
@movie_router.delete(
    path='/credits/{id}',
    tags=['Credit'],
    summary="Delete a credit with the ID",
    response_model=dict,
    status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result : CreditModel = db.query(CreditModel).filter(CreditModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message':'Cliente no registrado'})
    CrediService(db).delete_credito(id)
    return JSONResponse(status_code=200,content={"message":"Crédito eliminado"})