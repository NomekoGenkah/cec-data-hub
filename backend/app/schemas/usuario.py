"""Schemas de Usuario para la API."""
from pydantic import BaseModel


class UsuarioCreate(BaseModel):
    nombre: str
    email: str = ""
    rol: str = "vocal"


class UsuarioOut(BaseModel):
    id: str
    nombre: str
    email: str
    rol: str
