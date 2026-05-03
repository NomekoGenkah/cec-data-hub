"""
Agrupador de rutas: registra todos los módulos bajo el prefijo /api/v1.
"""
from fastapi import APIRouter

from app.modules.recursos.router import router as recursos_router
from app.modules.finanzas.router import router as finanzas_router
from app.modules.eventos.router import router as eventos_router
from app.modules.repositorio.router import router as repositorio_router
from app.modules.dispensador.router import router as dispensador_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(recursos_router)
api_router.include_router(finanzas_router)
api_router.include_router(eventos_router)
api_router.include_router(repositorio_router)
api_router.include_router(dispensador_router)
