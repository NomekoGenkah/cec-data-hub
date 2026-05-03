# Backend — CEC Data Hub

API RESTful construida con **FastAPI** y **MongoDB** (Motor async).

## Requisitos

- Python ≥ 3.11
- MongoDB Atlas URI (o MongoDB local)

## Instalación

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Variables de entorno

Crea un archivo `.env` en `backend/`:

```env
MONGODB_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/
MONGODB_DB=cec_data_hub
```

## Ejecutar

```bash
uvicorn app.main:app --reload
```

La documentación interactiva queda disponible en:
- Swagger UI → http://localhost:8000/docs
- Redoc      → http://localhost:8000/redoc

## Estructura

```
app/
├── main.py          # FastAPI app + lifespan
├── core/config.py   # Settings via pydantic-settings
├── db/mongodb.py    # Conexión Motor async
├── models/          # Modelos de datos
├── schemas/         # Schemas Pydantic (input/output)
├── services/        # Lógica de negocio
├── modules/         # Routers por módulo
└── routes/api.py    # Agrupador /api/v1
```
