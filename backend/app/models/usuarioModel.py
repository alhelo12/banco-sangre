import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum
from app.dbConfig.baseModels import Base


class RolEnum(str, enum.Enum):
    admin     = "admin"
    enfermero = "enfermero"
    medico    = "medico"


class Usuario(Base):
    __tablename__ = "usuarios"

    id         = Column(Integer, primary_key=True, index=True)
    nombre     = Column(String(100), nullable=False)
    email      = Column(String(100), unique=True, index=True, nullable=False)
    password   = Column(String(255), nullable=False)
    rol        = Column(Enum(RolEnum), default=RolEnum.enfermero, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
