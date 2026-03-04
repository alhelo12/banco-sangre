import enum
from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.dbConfig.baseModels import Base


class EstadoDonacion(str, enum.Enum):
    pendiente = "pendiente"
    aprobada  = "aprobada"
    rechazada = "rechazada"


class Donacion(Base):
    __tablename__ = "donaciones"

    id         = Column(Integer, primary_key=True, index=True)
    donante_id = Column(Integer, ForeignKey("donantes.id"), nullable=False)
    fecha      = Column(DateTime, default=datetime.utcnow)
    volumen_ml = Column(Float, default=450.0)
    estado     = Column(Enum(EstadoDonacion), default=EstadoDonacion.pendiente)
    notas      = Column(String(300))

    donante         = relationship("Donante", back_populates="donaciones")
    inventario_item = relationship("InventarioSangre", back_populates="donacion", uselist=False)
