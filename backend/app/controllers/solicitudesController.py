from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dbConfig.databaseSession import get_db
from app.models.solicitudModel import Solicitud
from app.schemas.solicitudSchema import SolicitudCreate, SolicitudOut, SolicitudUpdateEstado
from app.controllers.authController import get_current_user

router = APIRouter(
    prefix="/api/solicitudes",
    tags=["Solicitudes"],
    dependencies=[Depends(get_current_user)]
)


# ── GET /api/solicitudes ──────────────────────────────────
@router.get("/", response_model=List[SolicitudOut])
def listar_solicitudes(db: Session = Depends(get_db)):
    return db.query(Solicitud).all()


# ── GET /api/solicitudes/pendientes ──────────────────────
@router.get("/pendientes", response_model=List[SolicitudOut])
def listar_pendientes(db: Session = Depends(get_db)):
    return db.query(Solicitud).filter(Solicitud.estado == "pendiente").all()


# ── GET /api/solicitudes/{id} ─────────────────────────────
@router.get("/{id}", response_model=SolicitudOut)
def obtener_solicitud(id: int, db: Session = Depends(get_db)):
    solicitud = db.query(Solicitud).filter(Solicitud.id == id).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return solicitud


# ── POST /api/solicitudes ─────────────────────────────────
@router.post("/", response_model=SolicitudOut, status_code=201)
def crear_solicitud(data: SolicitudCreate, db: Session = Depends(get_db)):
    solicitud = Solicitud(**data.model_dump())
    db.add(solicitud)
    db.commit()
    db.refresh(solicitud)
    return solicitud


# ── PATCH /api/solicitudes/{id}/estado ───────────────────
@router.patch("/{id}/estado", response_model=SolicitudOut)
def actualizar_estado(id: int, data: SolicitudUpdateEstado, db: Session = Depends(get_db)):
    solicitud = db.query(Solicitud).filter(Solicitud.id == id).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    solicitud.estado = data.estado
    db.commit()
    db.refresh(solicitud)
    return solicitud


# ── DELETE /api/solicitudes/{id} ──────────────────────────
@router.delete("/{id}", status_code=204)
def eliminar_solicitud(id: int, db: Session = Depends(get_db)):
    solicitud = db.query(Solicitud).filter(Solicitud.id == id).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    db.delete(solicitud)
    db.commit()
