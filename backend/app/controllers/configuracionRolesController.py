from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from typing import Optional

from app.dbConfig.databaseSession import get_db
from app.models.configuracionRolModel import ConfiguracionRol
from app.models.usuarioModel import RolEnum
from app.controllers.authController import get_current_user

router = APIRouter(
    prefix="/api/configuracion-roles",
    tags=["Configuracion de Roles"],
    dependencies=[Depends(get_current_user)]
)


# ── Schemas locales ───────────────────────────────────────
class ConfiguracionRolCreate(BaseModel):
    prefijo:     str
    rol:         RolEnum
    descripcion: Optional[str] = None

class ConfiguracionRolOut(ConfiguracionRolCreate):
    id: int
    model_config = {"from_attributes": True}


# ── GET /api/configuracion-roles ──────────────────────────
@router.get("/", response_model=List[ConfiguracionRolOut])
def listar(db: Session = Depends(get_db)):
    return db.query(ConfiguracionRol).all()


# ── POST /api/configuracion-roles ─────────────────────────
@router.post("/", response_model=ConfiguracionRolOut, status_code=201)
def crear(data: ConfiguracionRolCreate, db: Session = Depends(get_db)):
    if db.query(ConfiguracionRol).filter(
        ConfiguracionRol.prefijo == data.prefijo.upper()
    ).first():
        raise HTTPException(status_code=400, detail="El prefijo ya existe")
    config = ConfiguracionRol(
        prefijo=data.prefijo.upper(),
        rol=data.rol,
        descripcion=data.descripcion
    )
    db.add(config)
    db.commit()
    db.refresh(config)
    return config


# ── PUT /api/configuracion-roles/{id} ─────────────────────
@router.put("/{id}", response_model=ConfiguracionRolOut)
def actualizar(id: int, data: ConfiguracionRolCreate, db: Session = Depends(get_db)):
    config = db.query(ConfiguracionRol).filter(ConfiguracionRol.id == id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuracion no encontrada")
    config.prefijo     = data.prefijo.upper()
    config.rol         = data.rol
    config.descripcion = data.descripcion
    db.commit()
    db.refresh(config)
    return config


# ── DELETE /api/configuracion-roles/{id} ──────────────────
@router.delete("/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(get_db)):
    config = db.query(ConfiguracionRol).filter(ConfiguracionRol.id == id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuracion no encontrada")
    db.delete(config)
    db.commit()


# ── GET /api/configuracion-roles/validar/{matricula} ──────
# Endpoint publico (sin login) para validar matriculas en el registro
@router.get("/validar/{matricula}", response_model=ConfiguracionRolOut, dependencies=[])
def validar_matricula(matricula: str, db: Session = Depends(get_db)):
    prefijo = matricula.split("-")[0].upper() if "-" in matricula else matricula.upper()
    config  = db.query(ConfiguracionRol).filter(
        ConfiguracionRol.prefijo == prefijo
    ).first()
    if not config:
        raise HTTPException(status_code=404, detail="Matricula no reconocida")
    return config
