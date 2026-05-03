"""
Módulo Recursos: CRUD base de la entidad Recurso.
Todos los demás módulos extienden esta lógica filtrando por `tipo`.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.mongodb import get_db
from app.schemas.recurso import RecursoCreate, RecursoUpdate, RecursoOut
from app.services import recurso_service

router = APIRouter(prefix="/recursos", tags=["Recursos"])


def _db() -> AsyncIOMotorDatabase:
    return get_db()


@router.get("/", response_model=list[RecursoOut])
async def listar(
    tipo: str | None = Query(default=None, description="Filtra por tipo de recurso"),
    tags: list[str] | None = Query(default=None, description="Filtra por uno o más tags"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: AsyncIOMotorDatabase = Depends(_db),
):
    return await recurso_service.listar_recursos(db, tipo=tipo, tags=tags, skip=skip, limit=limit)


@router.post("/", response_model=RecursoOut, status_code=201)
async def crear(payload: RecursoCreate, db: AsyncIOMotorDatabase = Depends(_db)):
    return await recurso_service.crear_recurso(db, payload)


@router.get("/{recurso_id}", response_model=RecursoOut)
async def obtener(recurso_id: str, db: AsyncIOMotorDatabase = Depends(_db)):
    doc = await recurso_service.obtener_recurso(db, recurso_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    return doc


@router.patch("/{recurso_id}", response_model=RecursoOut)
async def actualizar(
    recurso_id: str, payload: RecursoUpdate, db: AsyncIOMotorDatabase = Depends(_db)
):
    doc = await recurso_service.actualizar_recurso(db, recurso_id, payload)
    if not doc:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    return doc


@router.delete("/{recurso_id}", status_code=204)
async def eliminar(recurso_id: str, db: AsyncIOMotorDatabase = Depends(_db)):
    eliminado = await recurso_service.eliminar_recurso(db, recurso_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
