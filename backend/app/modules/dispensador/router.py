"""
Módulo Dispensador: gestiona productos de la máquina dispensadora.
Tipo de recurso: 'producto'.
La metadata incluye: precio, stock, slot, url_imagen.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.mongodb import get_db
from app.schemas.recurso import RecursoCreate, RecursoOut
from app.services import recurso_service

router = APIRouter(prefix="/dispensador", tags=["Dispensador"])


def _db() -> AsyncIOMotorDatabase:
    return get_db()


@router.get("/productos", response_model=list[RecursoOut])
async def listar_productos(
    db: AsyncIOMotorDatabase = Depends(_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
):
    """Lista todos los productos disponibles en la máquina dispensadora."""
    return await recurso_service.listar_recursos(db, tipo="producto", skip=skip, limit=limit)


@router.post("/productos", response_model=RecursoOut, status_code=201)
async def crear_producto(payload: RecursoCreate, db: AsyncIOMotorDatabase = Depends(_db)):
    """
    Registra un producto en la máquina dispensadora.
    Estructura sugerida para metadata:
        {
          "precio": 800,
          "stock": 10,
          "slot": "A1",
          "url_imagen": "https://..."
        }
    """
    payload.tipo = "producto"
    return await recurso_service.crear_recurso(db, payload)


@router.patch("/productos/{producto_id}/stock", response_model=RecursoOut)
async def ajustar_stock(
    producto_id: str,
    cantidad: int = Query(description="Diferencia de stock (positivo = recarga, negativo = despacho)"),
    db: AsyncIOMotorDatabase = Depends(_db),
):
    """Ajusta el stock de un producto sumando la `cantidad` indicada."""
    doc = await recurso_service.obtener_recurso(db, producto_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    nuevo_stock = doc.get("metadata", {}).get("stock", 0) + cantidad
    if nuevo_stock < 0:
        raise HTTPException(status_code=400, detail="Stock insuficiente")

    metadata = {**doc.get("metadata", {}), "stock": nuevo_stock}
    from app.schemas.recurso import RecursoUpdate
    return await recurso_service.actualizar_recurso(
        db, producto_id, RecursoUpdate(metadata=metadata)
    )
