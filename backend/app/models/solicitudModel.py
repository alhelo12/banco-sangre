import enum
from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, Enum
from sqlalchemy.orm import relationship
from app.dbConfig.baseModels import Base


class EstadoSolicitud(str, enum.Enum):
    pendiente = "pendiente"
    aprobada  = "aprobada"
    rechazada = "rechazada"
    entregada = "entregada"


class Solicitud(Base):
    __tablename__ = "solicitudes"

    id          = Column(Integer, primary_key=True, index=True)
    paciente    = Column(String(150), nullable=False)
    tipo_sangre = Column(String(5), nullable=False)
    volumen_ml  = Column(Float, nullable=False)
    medico      = Column(String(150))
    hospital    = Column(String(150))
    estado      = Column(Enum(EstadoSolicitud), default=EstadoSolicitud.pendiente)
    fecha       = Column(DateTime, default=datetime.utcnow)
    notas       = Column(String(300))

    transfusion = relationship("Transfusion", back_populates="solicitud", uselist=False)
