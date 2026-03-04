from pydantic import BaseModel
from datetime import date
from typing import Optional


class InventarioCreate(BaseModel):
    donacion_id: int
    tipo_sangre: str
    componente: str = "sangre total"
    volumen_ml: float
    fecha_exp: date


class InventarioOut(InventarioCreate):
    id: int
    disponible: bool

    model_config = {"from_attributes": True}


class InventarioUpdateDisponible(BaseModel):
    disponible: bool
