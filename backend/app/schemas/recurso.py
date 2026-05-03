"""
Schemas Pydantic para validación de entrada/salida de la API.
Separados del modelo de DB para no exponer campos internos (ej: _id).
"""
from datetime import datetime
from typing import Any

from pydantic import BaseModel


class AutorIn(BaseModel):
    id: str
    nombre: str
    rol: str


class RecursoCreate(BaseModel):
    """Payload para crear un nuevo Recurso."""
    tipo: str
    titulo: str
    descripcion: str = ""
    fecha: datetime | None = None
    autor: AutorIn | None = None
    tags: list[str] = []
    metadata: dict[str, Any] = {}
    estado: str = "activo"


class RecursoUpdate(BaseModel):
    """Campos opcionales para actualizar un Recurso existente."""
    titulo: str | None = None
    descripcion: str | None = None
    fecha: datetime | None = None
    tags: list[str] | None = None
    metadata: dict[str, Any] | None = None
    estado: str | None = None


class RecursoOut(BaseModel):
    """Representación del Recurso que devuelve la API."""
    id: str
    tipo: str
    titulo: str
    descripcion: str
    fecha: datetime
    autor: AutorIn | None = None
    tags: list[str]
    metadata: dict[str, Any]
    estado: str
