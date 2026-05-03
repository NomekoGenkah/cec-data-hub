"""
Configuración general de la aplicación.
Lee variables de entorno para conectarse a MongoDB Atlas u otras fuentes.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Título y versión expuestos en la documentación de FastAPI
    APP_TITLE: str = "CEC Data Hub API"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = (
        "API central del Centro de Estudiantes — arquitectura modular sobre MongoDB."
    )

    # Conexión MongoDB (Atlas o local)
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "cec_data_hub"


settings = Settings()
