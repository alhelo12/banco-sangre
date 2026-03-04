from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.solicitudModel import EstadoSolicitud


class SolicitudCreate(BaseModel):
    paciente: str
    tipo_sangre: str
    volumen_ml: float
    medico: Optional[str] = None
    hospital: Optional[str] = None
    notas: Optional[str] = None


class SolicitudOut(SolicitudCreate):
    id: int
    estado: EstadoSolicitud
    fecha: datetime

    model_config = {"from_attributes": True}


class SolicitudUpdateEstado(BaseModel):
    estado: EstadoSolicitud
