from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.donacionModel import EstadoDonacion


class DonacionCreate(BaseModel):
    donante_id: int
    volumen_ml: float = 450.0
    estado: EstadoDonacion = EstadoDonacion.pendiente
    notas: Optional[str] = None


class DonacionOut(DonacionCreate):
    id: int
    fecha: datetime

    model_config = {"from_attributes": True}


class DonacionUpdateEstado(BaseModel):
    estado: EstadoDonacion
