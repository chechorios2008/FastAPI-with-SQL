from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

@movie_router.get(
    path='/movies',
    tags=['Movies'],
    summary="Show all movies",
    response_model=List[Movie],
    status_code=200,
    dependencies= [Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result)) 

@movie_router.get('/movies/{id}', 
    tags=['Movies'],
    summary="Show a movie with the ID",
    response_model=Movie,
    status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message':'Pelicula no registrada en la BD actual.'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get(
    path='/movies/',
    tags=['Movies'],
    summary="Show movie by category",
    response_model= List[Movie],
    status_code=200)
def get_movie_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies_gy_category(category)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post(
    path='/movies',
    tags=['Movies'],
    summary="Create a movie in the list.",
    response_model=dict,
    status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201,content={"message":"Your movie has been REGISTERED!!!"})

@movie_router.put(
    path='/movies/{id}',
    tags=['Movies'],
    summary="Modifique a movie in the list",
    response_model=dict,
    status_code=200)
def update_movies(id:int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message':'Pelicula no registrada en la BD actual.'})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message":"Your movie has been MODIFIED!!!"})            
            
@movie_router.delete(
    path='/movies/{id}',
    tags=['Movies'],
    summary="Delete a movie with the ID",
    response_model=dict,
    status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message':'Pelicula no registrada en la BD actual.'})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200,content={"message":"Your movie has been DELETED!!!"})