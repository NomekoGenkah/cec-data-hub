# CEC Data Hub

Sistema de información modular para el **Centro de Estudiantes universitario**, construido sobre una arquitectura unificada con MongoDB.

## Tecnologías

| Capa | Tecnología |
|---|---|
| Backend | Python · FastAPI · Motor (async MongoDB) |
| Base de datos | MongoDB Atlas (o local) |
| Frontend | React · Vite · Tailwind CSS |
| Hardware | Arduino (C++) + simulador Python |

---

## Estructura del repositorio

```
cec-data-hub/
├── backend/            # API FastAPI + lógica de negocio
│   ├── app/
│   │   ├── main.py
│   │   ├── core/       # configuración (settings)
│   │   ├── db/         # conexión MongoDB (Motor)
│   │   ├── models/     # modelos de datos
│   │   ├── schemas/    # validaciones Pydantic
│   │   ├── services/   # lógica de negocio
│   │   ├── modules/    # módulos: recursos, finanzas, eventos, repositorio, dispensador
│   │   └── routes/     # agrupador de endpoints /api/v1
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/           # SPA React + Vite + Tailwind
│   ├── src/
│   │   ├── App.jsx
│   │   ├── pages/      # Dashboard, Recursos, Finanzas, Eventos
│   │   ├── components/ # Navbar, StatCard, FiltroRecursos
│   │   ├── services/   # cliente axios (/api/v1)
│   │   ├── hooks/      # useRecursos
│   │   └── utils/      # formatters (CLP, fechas, colores)
│   └── Dockerfile
│
├── hardware/
│   └── dispensador/
│       ├── arduino/    # dispensador.ino (C++)
│       ├── simulacion/ # simulador.py (sin hardware)
│       └── docs/
│
├── scripts/
│   ├── seed_data.py    # pobla MongoDB con datos de ejemplo
│   └── test_queries.py # consultas de prueba + comparación SQL
│
├── docs/
│   ├── arquitectura.md
│   ├── modelo_datos.md
│   └── comparacion_sql_vs_nosql.md
│
└── docker/
    └── docker-compose.yml
```

---

## Cómo ejecutar el sistema

### Opción A — Desarrollo local (sin Docker)

#### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Crea backend/.env con tu URI de MongoDB
echo "MONGODB_URI=mongodb://localhost:27017" > .env
echo "MONGODB_DB=cec_data_hub" >> .env

uvicorn app.main:app --reload
```

API disponible en http://localhost:8000  
Documentación: http://localhost:8000/docs

#### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

UI disponible en http://localhost:5173

#### 3. Poblar con datos de ejemplo

```bash
python scripts/seed_data.py
```

#### 4. Ejecutar consultas de prueba

```bash
python scripts/test_queries.py
```

---

### Opción B — Docker Compose

```bash
# Copia las variables de entorno (opcional: edita para usar Atlas)
cp backend/.env.example backend/.env

cd docker
docker compose up --build
```

- Backend → http://localhost:8000
- Frontend → http://localhost:5173
- MongoDB local → puerto 27017

---

## Endpoints principales (API v1)

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/v1/recursos` | Lista recursos (filtros: tipo, tags) |
| POST | `/api/v1/recursos` | Crea un recurso |
| GET | `/api/v1/recursos/{id}` | Obtiene un recurso |
| PATCH | `/api/v1/recursos/{id}` | Actualiza un recurso |
| DELETE | `/api/v1/recursos/{id}` | Elimina un recurso |
| GET | `/api/v1/finanzas` | Lista finanzas |
| GET | `/api/v1/finanzas/resumen` | Resumen por mes (agregación) |
| POST | `/api/v1/finanzas` | Registra transacción |
| GET | `/api/v1/eventos` | Lista eventos |
| POST | `/api/v1/eventos` | Crea evento |
| GET | `/api/v1/repositorio` | Lista documentos académicos |
| POST | `/api/v1/repositorio` | Sube referencia de documento |
| GET | `/api/v1/dispensador/productos` | Lista productos |
| POST | `/api/v1/dispensador/productos` | Registra producto |
| PATCH | `/api/v1/dispensador/productos/{id}/stock` | Ajusta stock |
| GET | `/health` | Estado del servidor |

---

## Modelo de datos

Ver [`docs/modelo_datos.md`](docs/modelo_datos.md) para la estructura completa de documentos y ejemplos.

Ver [`docs/comparacion_sql_vs_nosql.md`](docs/comparacion_sql_vs_nosql.md) para la comparación académica SQL vs MongoDB.
