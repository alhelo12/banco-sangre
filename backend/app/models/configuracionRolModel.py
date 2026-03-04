from sqlalchemy import Column, Integer, String, Enum
from app.dbConfig.baseModels import Base
from app.models.usuarioModel import RolEnum


class ConfiguracionRol(Base):
    __tablename__ = "configuracion_roles"

    id          = Column(Integer, primary_key=True, index=True)
    prefijo     = Column(String(20), unique=True, nullable=False)  # Ej: MED, ENF
    rol         = Column(Enum(RolEnum), nullable=False)             # medico, enfermero
    descripcion = Column(String(100))                               # Ej: Personal medico
