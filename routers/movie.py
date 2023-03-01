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

movie_router = APIRouter()

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="Mi pelicula", min_length=5, max_length=15)
    overview: str = Field(default="Descripción", min_length=15, max_length=50)
    year: int = Field(default=2022, le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=4, max_length=15)
#Clase para enviar información por defesto. 
    class Config:
        schema_extra = {
            "example": {
                "id":4,
                "title":"Mi pelicula",
                "overview":"Descripción de la pelicula",
                "year":2000,
                "rating":1.1,
                "category":"Arte"
            }
        }

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
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post(
    path='/movies',
    tags=['Movies'],
    summary="Create a movie in the list.",
    response_model=dict,
    status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201,content={"message":"Your movie has been REGISTERED!!!"})

@movie_router.put(
    path='/movies/{id}',
    tags=['Movies'],
    summary="Modifique a movie in the list",
    response_model=dict,
    status_code=200)
def update_movies(id:int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message':'Pelicula no registrada en la BD actual.'})
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
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