from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dbConfig.databaseSession import get_db
from app.models.donacionModel import Donacion
from app.schemas.donacionSchema import DonacionCreate, DonacionOut, DonacionUpdateEstado
from app.controllers.authController import get_current_user

router = APIRouter(
    prefix="/api/donaciones",
    tags=["Donaciones"],
    dependencies=[Depends(get_current_user)]
)


# ── GET /api/donaciones ───────────────────────────────────
@router.get("/", response_model=List[DonacionOut])
def listar_donaciones(db: Session = Depends(get_db)):
    return db.query(Donacion).all()


# ── GET /api/donaciones/{id} ──────────────────────────────
@router.get("/{id}", response_model=DonacionOut)
def obtener_donacion(id: int, db: Session = Depends(get_db)):
    donacion = db.query(Donacion).filter(Donacion.id == id).first()
    if not donacion:
        raise HTTPException(status_code=404, detail="Donacion no encontrada")
    return donacion


# ── POST /api/donaciones ──────────────────────────────────
@router.post("/", response_model=DonacionOut, status_code=201)
def crear_donacion(data: DonacionCreate, db: Session = Depends(get_db)):
    donacion = Donacion(**data.model_dump())
    db.add(donacion)
    db.commit()
    db.refresh(donacion)
    return donacion


# ── PATCH /api/donaciones/{id}/estado ────────────────────
@router.patch("/{id}/estado", response_model=DonacionOut)
def actualizar_estado(id: int, data: DonacionUpdateEstado, db: Session = Depends(get_db)):
    donacion = db.query(Donacion).filter(Donacion.id == id).first()
    if not donacion:
        raise HTTPException(status_code=404, detail="Donacion no encontrada")
    donacion.estado = data.estado
    db.commit()
    db.refresh(donacion)
    return donacion


# ── DELETE /api/donaciones/{id} ───────────────────────────
@router.delete("/{id}", status_code=204)
def eliminar_donacion(id: int, db: Session = Depends(get_db)):
    donacion = db.query(Donacion).filter(Donacion.id == id).first()
    if not donacion:
        raise HTTPException(status_code=404, detail="Donacion no encontrada")
    db.delete(donacion)
    db.commit()
