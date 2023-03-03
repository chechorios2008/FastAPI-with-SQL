from pydantic import BaseModel, Field
from typing import Optional, List


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