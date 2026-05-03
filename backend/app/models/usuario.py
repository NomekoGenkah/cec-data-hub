"""
Modelo de Usuario del sistema.
"""
from pydantic import BaseModel, Field


class Usuario(BaseModel):
    """
    Representa a un miembro del centro de estudiantes.
    El campo `rol` controla permisos (admin, tesorero, vocal, etc.).
    """
    id: str | None = Field(default=None, alias="_id")
    nombre: str
    email: str = ""
    rol: str = "vocal"

    class Config:
        populate_by_name = True
