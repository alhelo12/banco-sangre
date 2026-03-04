from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dbConfig.databaseSession import get_db
from app.models.donanteModel import Donante
from app.schemas.donanteSchema import DonanteCreate, DonanteOut
from app.controllers.authController import get_current_user

router = APIRouter(
    prefix="/api/donantes",
    tags=["Donantes"],
    dependencies=[Depends(get_current_user)]  # todas las rutas requieren login
)


# ── GET /api/donantes ─────────────────────────────────────
@router.get("/", response_model=List[DonanteOut])
def listar_donantes(db: Session = Depends(get_db)):
    return db.query(Donante).all()


# ── GET /api/donantes/{id} ────────────────────────────────
@router.get("/{id}", response_model=DonanteOut)
def obtener_donante(id: int, db: Session = Depends(get_db)):
    donante = db.query(Donante).filter(Donante.id == id).first()
    if not donante:
        raise HTTPException(status_code=404, detail="Donante no encontrado")
    return donante


# ── POST /api/donantes ────────────────────────────────────
@router.post("/", response_model=DonanteOut, status_code=201)
def crear_donante(data: DonanteCreate, db: Session = Depends(get_db)):
    donante = Donante(**data.model_dump())
    db.add(donante)
    db.commit()
    db.refresh(donante)
    return donante


# ── PUT /api/donantes/{id} ────────────────────────────────
@router.put("/{id}", response_model=DonanteOut)
def actualizar_donante(id: int, data: DonanteCreate, db: Session = Depends(get_db)):
    donante = db.query(Donante).filter(Donante.id == id).first()
    if not donante:
        raise HTTPException(status_code=404, detail="Donante no encontrado")
    for key, value in data.model_dump().items():
        setattr(donante, key, value)
    db.commit()
    db.refresh(donante)
    return donante


# ── DELETE /api/donantes/{id} ─────────────────────────────
@router.delete("/{id}", status_code=204)
def eliminar_donante(id: int, db: Session = Depends(get_db)):
    donante = db.query(Donante).filter(Donante.id == id).first()
    if not donante:
        raise HTTPException(status_code=404, detail="Donante no encontrado")
    db.delete(donante)
    db.commit()
