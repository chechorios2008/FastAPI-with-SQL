from pydantic import BaseModel, Field
from typing import Optional, List


class Credito(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(min_length=1, max_length=15)
    estado: str = Field(min_length=1, max_length=50)
    ingresos: int = Field()
    score: float = Field(ge=1, le=10)
    centralesRiesgo: str = Field(min_length=1, max_length=30)
