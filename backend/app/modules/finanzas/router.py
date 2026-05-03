"""
Módulo Finanzas: crea y consulta recursos de tipo 'finanza'.
La metadata de una finanza incluye: subtipo, monto, anio, mes, comprobante.
"""
from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.mongodb import get_db
from app.schemas.recurso import RecursoCreate, RecursoOut
from app.services import recurso_service

router = APIRouter(prefix="/finanzas", tags=["Finanzas"])


def _db() -> AsyncIOMotorDatabase:
    return get_db()


@router.get("/", response_model=list[RecursoOut])
async def listar_finanzas(
    db: AsyncIOMotorDatabase = Depends(_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
):
    """Retorna todos los recursos cuyo tipo es 'finanza'."""
    return await recurso_service.listar_recursos(db, tipo="finanza", skip=skip, limit=limit)


@router.post("/", response_model=RecursoOut, status_code=201)
async def crear_finanza(payload: RecursoCreate, db: AsyncIOMotorDatabase = Depends(_db)):
    """
    Crea una transacción financiera.
    Estructura sugerida para metadata:
        {
          "subtipo": "ingreso" | "egreso",
          "monto": 50000,
          "anio": 2024,
          "mes": 5,
          "comprobante": "https://..."
        }
    """
    payload.tipo = "finanza"
    return await recurso_service.crear_recurso(db, payload)


@router.get("/resumen", summary="Resumen financiero por mes")
async def resumen(
    anio: int | None = Query(default=None),
    mes: int | None = Query(default=None),
    db: AsyncIOMotorDatabase = Depends(_db),
):
    """
    Agrupación de montos por mes y subtipo (ingreso/egreso).
    Ejemplo de uso: GET /finanzas/resumen?anio=2024
    """
    return await recurso_service.agregar_finanzas(db, anio=anio, mes=mes)
