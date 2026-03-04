from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dbConfig.databaseSession import get_db
from app.models.usuarioModel import Usuario
from app.schemas.authSchema import UsuarioCreate, UsuarioOut
from app.core.security import hash_password
from app.controllers.authController import get_current_user

router = APIRouter(
    prefix="/api/usuarios",
    tags=["Usuarios"],
    dependencies=[Depends(get_current_user)]
)


# ── GET /api/usuarios ─────────────────────────────────────
@router.get("/", response_model=List[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


# ── GET /api/usuarios/{id} ────────────────────────────────
@router.get("/{id}", response_model=UsuarioOut)
def obtener_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


# ── POST /api/usuarios ────────────────────────────────────
@router.post("/", response_model=UsuarioOut, status_code=201)
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == data.email).first():
        raise HTTPException(status_code=400, detail="El email ya esta registrado")
    usuario = Usuario(
        nombre=data.nombre,
        email=data.email,
        password=hash_password(data.password),
        rol=data.rol,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


# ── PUT /api/usuarios/{id} ────────────────────────────────
@router.put("/{id}", response_model=UsuarioOut)
def actualizar_usuario(id: int, data: UsuarioCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.nombre = data.nombre
    usuario.email  = data.email
    usuario.rol    = data.rol
    if data.password:
        usuario.password = hash_password(data.password)
    db.commit()
    db.refresh(usuario)
    return usuario


# ── DELETE /api/usuarios/{id} ─────────────────────────────
@router.delete("/{id}", status_code=204)
def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
