"""
Gestión de la conexión a MongoDB usando Motor (driver async).
Se usa un cliente global que se inicializa al arrancar FastAPI y se cierra al apagar.
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

_client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient:
    """Retorna el cliente Motor activo."""
    if _client is None:
        raise RuntimeError("La base de datos no ha sido inicializada. Llama a connect_db() primero.")
    return _client


def get_db() -> AsyncIOMotorDatabase:
    """Retorna la base de datos activa."""
    return get_client()[settings.MONGODB_DB]


async def connect_db() -> None:
    """Abre la conexión al iniciar la aplicación (lifespan)."""
    global _client
    _client = AsyncIOMotorClient(settings.MONGODB_URI)


async def close_db() -> None:
    """Cierra la conexión al apagar la aplicación (lifespan)."""
    global _client
    if _client:
        _client.close()
        _client = None
