from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from app.dbConfig.baseModels import Base


class Donante(Base):
    __tablename__ = "donantes"

    id          = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String(100), nullable=False)
    apellido    = Column(String(100), nullable=False)
    fecha_nac   = Column(Date, nullable=False)
    tipo_sangre = Column(String(5), nullable=False)
    telefono    = Column(String(20))
    email       = Column(String(100))
    created_at  = Column(DateTime, default=datetime.utcnow)

    donaciones  = relationship("Donacion", back_populates="donante")
