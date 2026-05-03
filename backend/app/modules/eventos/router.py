"""
Módulo Eventos: crea y consulta recursos de tipo 'evento'.
La metadata de un evento incluye: lugar, capacidad, asistentes, url_imagen.
"""
from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.mongodb import get_db
from app.schemas.recurso import RecursoCreate, RecursoOut
from app.services import recurso_service

router = APIRouter(prefix="/eventos", tags=["Eventos"])


def _db() -> AsyncIOMotorDatabase:
    return get_db()


@router.get("/", response_model=list[RecursoOut])
async def listar_eventos(
    db: AsyncIOMotorDatabase = Depends(_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
):
    return await recurso_service.listar_recursos(db, tipo="evento", skip=skip, limit=limit)


@router.post("/", response_model=RecursoOut, status_code=201)
async def crear_evento(payload: RecursoCreate, db: AsyncIOMotorDatabase = Depends(_db)):
    """
    Crea un evento.
    Estructura sugerida para metadata:
        {
          "lugar": "Sala B",
          "capacidad": 100,
          "asistentes": 0,
          "url_imagen": "https://..."
        }
    """
    payload.tipo = "evento"
    return await recurso_service.crear_recurso(db, payload)
