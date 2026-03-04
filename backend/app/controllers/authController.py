from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.dbConfig.databaseSession import get_db
from app.models.usuarioModel import Usuario, RolEnum
from app.models.configuracionRolModel import ConfiguracionRol
from app.schemas.authSchema import UsuarioOut, Token
from app.core.security import hash_password, verify_password, create_access_token, decode_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


# ── Schema de registro con matricula ─────────────────────
class RegistroConMatricula(BaseModel):
    nombre:    str
    email:     EmailStr
    password:  str
    matricula: str


# ── Dependency: obtener usuario autenticado desde el token ──
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    try:
        payload = decode_token(token)
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Token invalido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalido o expirado")

    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user


# ── POST /api/auth/register ───────────────────────────────
@router.post("/register", response_model=UsuarioOut, status_code=201)
def register(data: RegistroConMatricula, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == data.email).first():
        raise HTTPException(status_code=400, detail="El email ya esta registrado")

    # Validar la matricula y obtener el rol
    prefijo = data.matricula.split("-")[0].upper() if "-" in data.matricula else data.matricula.upper()
    config  = db.query(ConfiguracionRol).filter(ConfiguracionRol.prefijo == prefijo).first()
    if not config:
        raise HTTPException(status_code=400, detail="Matricula no reconocida. Contacta al administrador")

    user = Usuario(
        nombre=data.nombre,
        email=data.email,
        password=hash_password(data.password),
        rol=config.rol,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ── POST /api/auth/token (login) ──────────────────────────
@router.post("/token", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == form.username).first()
    if not user or not verify_password(form.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token({"sub": user.email, "rol": user.rol})
    return {"access_token": token}


# ── GET /api/auth/me ──────────────────────────────────────
@router.get("/me", response_model=UsuarioOut)
def me(current_user: Usuario = Depends(get_current_user)):
    return current_user


# ── GET /api/auth/validar-matricula/{matricula} ───────────
# Endpoint publico para validar matriculas en el registro
@router.get("/validar-matricula/{matricula}")
def validar_matricula(matricula: str, db: Session = Depends(get_db)):
    prefijo = matricula.split("-")[0].upper() if "-" in matricula else matricula.upper()
    config  = db.query(ConfiguracionRol).filter(ConfiguracionRol.prefijo == prefijo).first()
    if not config:
        raise HTTPException(status_code=404, detail="Matricula no reconocida")
    return {"prefijo": config.prefijo, "rol": config.rol, "descripcion": config.descripcion}
