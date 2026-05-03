"""
seed_data.py
------------
Pobla la base de datos MongoDB con datos de ejemplo para desarrollo y demostración.

Uso:
    python scripts/seed_data.py

Variables de entorno (opcionales, por defecto usa localhost):
    MONGODB_URI=mongodb+srv://...
    MONGODB_DB=cec_data_hub
"""
import asyncio
import os
from datetime import datetime, timedelta

from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB  = os.getenv("MONGODB_DB",  "cec_data_hub")

# ── Documentos de ejemplo ──────────────────────────────────────────────────

AUTOR_DEFAULT = {"id": "user001", "nombre": "Admin CEC", "rol": "admin"}

RECURSOS = [
    # ── Finanzas ──────────────────────────────────────────────────────────
    {
        "tipo": "finanza", "titulo": "Cuota socios — Mayo 2024",
        "descripcion": "Recaudación mensual de cuotas de socios.",
        "fecha": datetime(2024, 5, 1), "autor": AUTOR_DEFAULT,
        "tags": ["cuota", "mensual"],
        "metadata": {"subtipo": "ingreso", "monto": 150000, "anio": 2024, "mes": 5},
        "estado": "activo",
    },
    {
        "tipo": "finanza", "titulo": "Compra materiales evento",
        "descripcion": "Materiales para la semana de integración.",
        "fecha": datetime(2024, 5, 10), "autor": AUTOR_DEFAULT,
        "tags": ["evento", "gasto"],
        "metadata": {"subtipo": "egreso", "monto": 45000, "anio": 2024, "mes": 5},
        "estado": "activo",
    },
    {
        "tipo": "finanza", "titulo": "Bingo recaudatorio",
        "descripcion": "Ingresos del bingo de junio.",
        "fecha": datetime(2024, 6, 15), "autor": AUTOR_DEFAULT,
        "tags": ["actividad", "recaudacion"],
        "metadata": {"subtipo": "ingreso", "monto": 280000, "anio": 2024, "mes": 6},
        "estado": "activo",
    },
    # ── Eventos ───────────────────────────────────────────────────────────
    {
        "tipo": "evento", "titulo": "Semana de Integración 2024",
        "descripcion": "Actividades de bienvenida para estudiantes de primer año.",
        "fecha": datetime(2024, 3, 18), "autor": AUTOR_DEFAULT,
        "tags": ["bienvenida", "primer_anio"],
        "metadata": {"lugar": "Patio central", "capacidad": 200, "asistentes": 175},
        "estado": "activo",
    },
    {
        "tipo": "evento", "titulo": "Charla: Becas y beneficios universitarios",
        "descripcion": "Información sobre postulación a becas JUNAEB y créditos.",
        "fecha": datetime.utcnow() + timedelta(days=7), "autor": AUTOR_DEFAULT,
        "tags": ["becas", "informacion"],
        "metadata": {"lugar": "Sala A-301", "capacidad": 60, "asistentes": 0},
        "estado": "activo",
    },
    # ── Documentos ────────────────────────────────────────────────────────
    {
        "tipo": "documento", "titulo": "Apuntes Cálculo I — 2023",
        "descripcion": "Resumen de límites, derivadas e integrales.",
        "fecha": datetime(2023, 11, 30), "autor": {"id": "u002", "nombre": "Juan P.", "rol": "vocal"},
        "tags": ["calculo", "matematicas", "primer_anio"],
        "metadata": {
            "url": "https://drive.google.com/file/example",
            "tipo_archivo": "pdf",
            "asignatura": "Cálculo I",
            "carrera": "Ingeniería Civil",
        },
        "estado": "activo",
    },
    {
        "tipo": "documento", "titulo": "Guía de laboratorio Física II",
        "descripcion": "Procedimientos para los laboratorios del segundo semestre.",
        "fecha": datetime(2024, 4, 1), "autor": {"id": "u003", "nombre": "Ana G.", "rol": "vocal"},
        "tags": ["fisica", "laboratorio"],
        "metadata": {
            "url": "https://drive.google.com/file/example2",
            "tipo_archivo": "pdf",
            "asignatura": "Física II",
            "carrera": "Ingeniería Civil",
        },
        "estado": "activo",
    },
    # ── Productos dispensadora ────────────────────────────────────────────
    {
        "tipo": "producto", "titulo": "Agua mineral 500 ml",
        "descripcion": "Botella de agua sin gas.",
        "fecha": datetime.utcnow(), "autor": AUTOR_DEFAULT,
        "tags": ["bebida", "agua"],
        "metadata": {"precio": 800, "stock": 15, "slot": "A1"},
        "estado": "activo",
    },
    {
        "tipo": "producto", "titulo": "Barra de cereal",
        "descripcion": "Barra de cereal con avena y miel.",
        "fecha": datetime.utcnow(), "autor": AUTOR_DEFAULT,
        "tags": ["snack", "cereal"],
        "metadata": {"precio": 600, "stock": 10, "slot": "A2"},
        "estado": "activo",
    },
    {
        "tipo": "producto", "titulo": "Jugo de naranja 250 ml",
        "descripcion": "Jugo de naranja en caja.",
        "fecha": datetime.utcnow(), "autor": AUTOR_DEFAULT,
        "tags": ["bebida", "jugo"],
        "metadata": {"precio": 700, "stock": 8, "slot": "B1"},
        "estado": "activo",
    },
]


async def seed():
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[MONGODB_DB]

    # Limpia colección antes de insertar
    await db["recursos"].delete_many({})
    result = await db["recursos"].insert_many(RECURSOS)
    print(f"✓ Insertados {len(result.inserted_ids)} documentos en '{MONGODB_DB}.recursos'")

    # Índices sugeridos para consultas frecuentes
    await db["recursos"].create_index("tipo")
    await db["recursos"].create_index("tags")
    await db["recursos"].create_index([("tipo", 1), ("fecha", -1)])
    print("✓ Índices creados: tipo, tags, (tipo, fecha)")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
