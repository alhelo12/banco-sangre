from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.dbConfig.databaseSession import engine
from app.dbConfig.baseModels import Base

# Importar todos los modelos para que SQLAlchemy los registre
from app.models import usuarioModel, donanteModel, donacionModel
from app.models import inventarioModel, solicitudModel, transfusionModel
from app.controllers import authController, donantesController, donacionesController, inventarioController, solicitudesController

# Crea las tablas en la BD si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Banco de Sangre API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["Health"])
def health():
    return {"status": "ok", "message": "Banco de Sangre API funcionando"}

app.include_router(authController.router)
app.include_router(donantesController.router)
app.include_router(donacionesController.router)
app.include_router(inventarioController.router)
app.include_router(solicitudesController.router)
