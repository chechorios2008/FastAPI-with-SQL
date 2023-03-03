from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from utils.jwt_manager import create_token
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "My aplication with FastAPI"
app.version = "0.0.1"

#Importación de modulos externos. 
app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine) #
        
movies = [
    {
            "id":1,
            "title":"Avatar",
            "overview":"In this movie a amaizin blue people that other word try to save their land, and a human help ther",
            "year":2009,
            "rating":7.8,
            "category":"Action"
        },
    {
            "id":2,
            "title":"Titanic",
            "overview":"History of bigger ship of the word in those moment, and love history of two young lovers",
            "year":1999,
            "rating":8.8,
            "category":"Drama"
        },
    {
            "id":3,
            "title":"Iron Man",
            "overview":"Millionary man with make a super metal suit and help or word",
            "year":2010,
            "rating":6.8,
            "category":"Action"
        }
]

@app.get(
    path='/', 
    tags = ['Home'], 
    summary="Home of page")
def message():
    return HTMLResponse ("<h2> Hello myt Best friend, in this page there are amazin movies. </h2>")