"""
Modelos de datos de MongoDB.
Recurso es la entidad principal del sistema; todos los módulos operan sobre ella.
"""
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field
from bson import ObjectId


class AutorEmbebido(BaseModel):
    """Autor embebido dentro de un Recurso (evita JOIN con colección Usuario)."""
    id: str
    nombre: str
    rol: str


class Recurso(BaseModel):
    """
    Entidad principal del sistema CEC Data Hub.

    El campo `tipo` distingue el módulo al que pertenece:
        - finanza
        - evento
        - documento
        - producto      (máquina dispensadora)
        - otro

    El campo `metadata` es un objeto flexible (schema-less) que cada módulo
    rellena con la información específica que necesita, sin requerir migraciones.
    """
    id: str | None = Field(default=None, alias="_id")
    tipo: str
    titulo: str
    descripcion: str = ""
    fecha: datetime = Field(default_factory=datetime.utcnow)
    autor: AutorEmbebido | None = None
    tags: list[str] = []
    metadata: dict[str, Any] = {}
    estado: str = "activo"

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
