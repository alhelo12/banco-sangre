from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dbConfig.databaseSession import get_db
from app.models.transfusionModel import Transfusion
from app.models.inventarioModel import InventarioSangre
from app.models.solicitudModel import Solicitud
from app.schemas.transfusionSchema import TransfusionCreate, TransfusionOut
from app.controllers.authController import get_current_user

router = APIRouter(
    prefix="/api/transfusiones",
    tags=["Transfusiones"],
    dependencies=[Depends(get_current_user)]
)


# ── GET /api/transfusiones ────────────────────────────────
@router.get("/", response_model=List[TransfusionOut])
def listar_transfusiones(db: Session = Depends(get_db)):
    return db.query(Transfusion).all()


# ── GET /api/transfusiones/{id} ───────────────────────────
@router.get("/{id}", response_model=TransfusionOut)
def obtener_transfusion(id: int, db: Session = Depends(get_db)):
    transfusion = db.query(Transfusion).filter(Transfusion.id == id).first()
    if not transfusion:
        raise HTTPException(status_code=404, detail="Transfusion no encontrada")
    return transfusion


# ── POST /api/transfusiones ───────────────────────────────
@router.post("/", response_model=TransfusionOut, status_code=201)
def crear_transfusion(data: TransfusionCreate, db: Session = Depends(get_db)):

    # Verificar que la solicitud existe y esta aprobada
    solicitud = db.query(Solicitud).filter(Solicitud.id == data.solicitud_id).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    if solicitud.estado != "aprobada":
        raise HTTPException(status_code=400, detail="La solicitud debe estar aprobada para registrar una transfusion")

    # Verificar que la unidad de inventario existe y esta disponible
    unidad = db.query(InventarioSangre).filter(InventarioSangre.id == data.inventario_id).first()
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad de inventario no encontrada")
    if not unidad.disponible:
        raise HTTPException(status_code=400, detail="La unidad de inventario ya fue utilizada")

    # Crear la transfusion
    transfusion = Transfusion(**data.model_dump())
    db.add(transfusion)

    # Marcar la unidad como no disponible
    unidad.disponible = False

    # Marcar la solicitud como entregada
    solicitud.estado = "entregada"

    db.commit()
    db.refresh(transfusion)
    return transfusion


# ── DELETE /api/transfusiones/{id} ────────────────────────
@router.delete("/{id}", status_code=204)
def eliminar_transfusion(id: int, db: Session = Depends(get_db)):
    transfusion = db.query(Transfusion).filter(Transfusion.id == id).first()
    if not transfusion:
        raise HTTPException(status_code=404, detail="Transfusion no encontrada")
    db.delete(transfusion)
    db.commit()
