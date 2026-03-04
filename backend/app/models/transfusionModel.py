from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.dbConfig.baseModels import Base


class Transfusion(Base):
    __tablename__ = "transfusiones"

    id            = Column(Integer, primary_key=True, index=True)
    solicitud_id  = Column(Integer, ForeignKey("solicitudes.id"), nullable=False)
    inventario_id = Column(Integer, ForeignKey("inventario_sangre.id"), nullable=False)
    fecha         = Column(DateTime, default=datetime.utcnow)
    realizada_por = Column(String(150))
    observaciones = Column(String(300))

    solicitud     = relationship("Solicitud", back_populates="transfusion")
