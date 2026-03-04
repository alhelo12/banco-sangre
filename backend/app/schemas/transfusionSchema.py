from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TransfusionCreate(BaseModel):
    solicitud_id: int
    inventario_id: int
    realizada_por: Optional[str] = None
    observaciones: Optional[str] = None


class TransfusionOut(TransfusionCreate):
    id: int
    fecha: datetime

    model_config = {"from_attributes": True}
