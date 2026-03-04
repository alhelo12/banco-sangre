from pydantic import BaseModel, EmailStr
from app.models.usuarioModel import RolEnum


class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    rol: RolEnum = RolEnum.enfermero


class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    rol: RolEnum

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
