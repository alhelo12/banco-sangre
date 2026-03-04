from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dbConfig.databaseSession import get_db
from app.models.inventarioModel import InventarioSangre
from app.schemas.inventarioSchema import InventarioCreate, InventarioOut, InventarioUpdateDisponible
from app.controllers.authController import get_current_user

router = APIRouter(
    prefix="/api/inventario",
    tags=["Inventario"],
    dependencies=[Depends(get_current_user)]
)


# ── GET /api/inventario ───────────────────────────────────
@router.get("/", response_model=List[InventarioOut])
def listar_inventario(db: Session = Depends(get_db)):
    return db.query(InventarioSangre).all()


# ── GET /api/inventario/disponible ───────────────────────
@router.get("/disponible", response_model=List[InventarioOut])
def listar_disponible(db: Session = Depends(get_db)):
    return db.query(InventarioSangre).filter(InventarioSangre.disponible == True).all()


# ── GET /api/inventario/{id} ──────────────────────────────
@router.get("/{id}", response_model=InventarioOut)
def obtener_unidad(id: int, db: Session = Depends(get_db)):
    unidad = db.query(InventarioSangre).filter(InventarioSangre.id == id).first()
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    return unidad


# ── POST /api/inventario ──────────────────────────────────
@router.post("/", response_model=InventarioOut, status_code=201)
def agregar_unidad(data: InventarioCreate, db: Session = Depends(get_db)):
    unidad = InventarioSangre(**data.model_dump())
    db.add(unidad)
    db.commit()
    db.refresh(unidad)
    return unidad


# ── PATCH /api/inventario/{id}/disponible ─────────────────
@router.patch("/{id}/disponible", response_model=InventarioOut)
def actualizar_disponible(id: int, data: InventarioUpdateDisponible, db: Session = Depends(get_db)):
    unidad = db.query(InventarioSangre).filter(InventarioSangre.id == id).first()
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    unidad.disponible = data.disponible
    db.commit()
    db.refresh(unidad)
    return unidad


# ── DELETE /api/inventario/{id} ───────────────────────────
@router.delete("/{id}", status_code=204)
def eliminar_unidad(id: int, db: Session = Depends(get_db)):
    unidad = db.query(InventarioSangre).filter(InventarioSangre.id == id).first()
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    db.delete(unidad)
    db.commit()
