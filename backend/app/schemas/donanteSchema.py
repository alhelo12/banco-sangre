from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class DonanteCreate(BaseModel):
    nombre: str
    apellido: str
    fecha_nac: date
    tipo_sangre: str
    telefono: Optional[str] = None
    email: Optional[str] = None


class DonanteOut(DonanteCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
