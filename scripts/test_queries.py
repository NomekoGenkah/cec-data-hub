"""
test_queries.py
---------------
Ejecuta consultas de prueba contra MongoDB para validar el modelo de datos
y comparar con el equivalente en SQL.

Uso:
    python scripts/test_queries.py

Variables de entorno:
    MONGODB_URI  (default: mongodb://localhost:27017)
    MONGODB_DB   (default: cec_data_hub)
"""
import asyncio
import os

from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB  = os.getenv("MONGODB_DB",  "cec_data_hub")


async def run_queries():
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[MONGODB_DB]
    col = db["recursos"]

    # ── 1. Listar todos los recursos ──────────────────────────────────────
    # SQL equivalente: SELECT * FROM recursos
    print("\n── 1. Todos los recursos ──────────────────────────────────────")
    async for doc in col.find({}, {"_id": 0, "titulo": 1, "tipo": 1}):
        print(f"  [{doc['tipo']:10}] {doc['titulo']}")

    # ── 2. Filtrar por tipo ───────────────────────────────────────────────
    # SQL: SELECT * FROM recursos WHERE tipo = 'evento'
    print("\n── 2. Solo eventos ────────────────────────────────────────────")
    async for doc in col.find({"tipo": "evento"}, {"_id": 0, "titulo": 1, "fecha": 1}):
        print(f"  {doc['titulo']} — {doc['fecha'].date()}")

    # ── 3. Búsqueda por tag ───────────────────────────────────────────────
    # SQL: JOIN con tabla recurso_tags + WHERE tag = 'becas'
    # NoSQL: array contains — más simple y sin JOIN
    print("\n── 3. Recursos con tag 'becas' ────────────────────────────────")
    async for doc in col.find({"tags": "becas"}, {"_id": 0, "titulo": 1, "tags": 1}):
        print(f"  {doc['titulo']} → {doc['tags']}")

    # ── 4. Suma de ingresos vs egresos ────────────────────────────────────
    # SQL: SELECT subtipo, SUM(monto) FROM finanzas GROUP BY subtipo
    # NoSQL: pipeline de agregación sobre metadata embebida
    print("\n── 4. Resumen financiero ───────────────────────────────────────")
    pipeline = [
        {"$match": {"tipo": "finanza"}},
        {"$group": {"_id": "$metadata.subtipo", "total": {"$sum": "$metadata.monto"}}},
    ]
    async for doc in col.aggregate(pipeline):
        print(f"  {doc['_id']:10} → $ {doc['total']:,}")

    # ── 5. Eventos con más asistentes ─────────────────────────────────────
    # SQL: SELECT titulo, asistentes FROM eventos ORDER BY asistentes DESC
    # NoSQL: sort sobre campo embebido
    print("\n── 5. Eventos por asistentes (desc) ───────────────────────────")
    async for doc in col.find(
        {"tipo": "evento"},
        {"_id": 0, "titulo": 1, "metadata.asistentes": 1},
    ).sort("metadata.asistentes", -1).limit(5):
        print(f"  {doc['titulo']} — {doc.get('metadata', {}).get('asistentes', 0)} asistentes")

    # ── 6. Stock de productos ─────────────────────────────────────────────
    # SQL: SELECT titulo, stock, precio FROM productos WHERE stock > 0
    print("\n── 6. Productos con stock disponible ──────────────────────────")
    async for doc in col.find(
        {"tipo": "producto", "metadata.stock": {"$gt": 0}},
        {"_id": 0, "titulo": 1, "metadata": 1},
    ):
        m = doc.get("metadata", {})
        print(f"  [{m.get('slot','?')}] {doc['titulo']} — stock: {m.get('stock')} — ${m.get('precio')}")

    client.close()
    print("\n✓ Todas las consultas ejecutadas correctamente.\n")


if __name__ == "__main__":
    asyncio.run(run_queries())
