"""
Servicio de Recursos: lógica de negocio sobre la colección `recursos` en MongoDB.
Centraliza todo el acceso a datos para que los routers sean delgados.
"""
from datetime import datetime
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.recurso import RecursoCreate, RecursoUpdate


COLLECTION = "recursos"


def _serialize(doc: dict) -> dict:
    """Convierte ObjectId a str para la respuesta JSON."""
    if doc and "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc


async def crear_recurso(db: AsyncIOMotorDatabase, payload: RecursoCreate) -> dict:
    doc = payload.model_dump()
    doc["fecha"] = doc.get("fecha") or datetime.utcnow()
    result = await db[COLLECTION].insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return doc


async def listar_recursos(
    db: AsyncIOMotorDatabase,
    tipo: str | None = None,
    tags: list[str] | None = None,
    skip: int = 0,
    limit: int = 50,
) -> list[dict]:
    """
    Filtra por tipo y/o tags.
    Los tags se buscan con $all (el documento debe tener TODOS los tags indicados).
    """
    filtro: dict[str, Any] = {}
    if tipo:
        filtro["tipo"] = tipo
    if tags:
        filtro["tags"] = {"$all": tags}

    cursor = db[COLLECTION].find(filtro).skip(skip).limit(limit)
    return [_serialize(doc) async for doc in cursor]


async def obtener_recurso(db: AsyncIOMotorDatabase, recurso_id: str) -> dict | None:
    doc = await db[COLLECTION].find_one({"_id": ObjectId(recurso_id)})
    return _serialize(doc) if doc else None


async def actualizar_recurso(
    db: AsyncIOMotorDatabase, recurso_id: str, payload: RecursoUpdate
) -> dict | None:
    cambios = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not cambios:
        return await obtener_recurso(db, recurso_id)
    await db[COLLECTION].update_one(
        {"_id": ObjectId(recurso_id)}, {"$set": cambios}
    )
    return await obtener_recurso(db, recurso_id)


async def eliminar_recurso(db: AsyncIOMotorDatabase, recurso_id: str) -> bool:
    result = await db[COLLECTION].delete_one({"_id": ObjectId(recurso_id)})
    return result.deleted_count == 1


async def agregar_finanzas(
    db: AsyncIOMotorDatabase, anio: int | None = None, mes: int | None = None
) -> list[dict]:
    """
    Agrupación de ingresos/egresos por mes.
    Solo considera recursos de tipo 'finanza'.
    """
    match: dict[str, Any] = {"tipo": "finanza"}
    if anio:
        match["metadata.anio"] = anio
    if mes:
        match["metadata.mes"] = mes

    pipeline = [
        {"$match": match},
        {
            "$group": {
                "_id": {
                    "anio": "$metadata.anio",
                    "mes": "$metadata.mes",
                    "subtipo": "$metadata.subtipo",
                },
                "total": {"$sum": "$metadata.monto"},
                "cantidad": {"$sum": 1},
            }
        },
        {"$sort": {"_id.anio": 1, "_id.mes": 1}},
    ]
    cursor = db[COLLECTION].aggregate(pipeline)
    return [doc async for doc in cursor]
