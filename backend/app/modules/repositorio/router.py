"""
Módulo Repositorio Académico: crea y consulta recursos de tipo 'documento'.
La metadata de un documento incluye: url, tipo_archivo, asignatura, carrera.
"""
from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.mongodb import get_db
from app.schemas.recurso import RecursoCreate, RecursoOut
from app.services import recurso_service

router = APIRouter(prefix="/repositorio", tags=["Repositorio"])


def _db() -> AsyncIOMotorDatabase:
    return get_db()


@router.get("/", response_model=list[RecursoOut])
async def listar_documentos(
    db: AsyncIOMotorDatabase = Depends(_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
):
    return await recurso_service.listar_recursos(db, tipo="documento", skip=skip, limit=limit)


@router.post("/", response_model=RecursoOut, status_code=201)
async def subir_documento(payload: RecursoCreate, db: AsyncIOMotorDatabase = Depends(_db)):
    """
    Registra un documento académico.
    Estructura sugerida para metadata:
        {
          "url": "https://drive.google.com/...",
          "tipo_archivo": "pdf",
          "asignatura": "Cálculo I",
          "carrera": "Ingeniería Civil"
        }
    """
    payload.tipo = "documento"
    return await recurso_service.crear_recurso(db, payload)
