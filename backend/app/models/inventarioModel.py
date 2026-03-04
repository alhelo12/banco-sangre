from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.dbConfig.baseModels import Base


class InventarioSangre(Base):
    __tablename__ = "inventario_sangre"

    id          = Column(Integer, primary_key=True, index=True)
    donacion_id = Column(Integer, ForeignKey("donaciones.id"), nullable=False)
    tipo_sangre = Column(String(5), nullable=False)
    componente  = Column(String(50), default="sangre total")
    volumen_ml  = Column(Float, nullable=False)
    fecha_exp   = Column(Date, nullable=False)
    disponible  = Column(Boolean, default=True)

    donacion    = relationship("Donacion", back_populates="inventario_item")
