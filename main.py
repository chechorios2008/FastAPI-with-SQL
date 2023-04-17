from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from utils.jwt_manager import create_token
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.credito import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "API: Intercambio de información de ventas y créditos."
app.version = "0.0.1"

#Importación de modulos externos. 
app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine) #
        

@app.get(
    path='/', 
    tags = ['Home'], 
    summary="Home of page")
def message():
    return HTMLResponse ("<h1> API: Intercambio de información de ventas y créditos.. </h1>")