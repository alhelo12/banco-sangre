from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = Field(
        ...,
        description="Ej: postgresql://usuario:password@localhost:5432/banco_sangre (ver backend/.env-example.txt)",
    )
    SECRET_KEY: str = Field(
        ...,
        min_length=32,
        description="Clave para firmar JWT. Genera una con: python -c 'import secrets; print(secrets.token_hex(32))'",
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
