# Arquitectura del Sistema — CEC Data Hub

## Visión general

CEC Data Hub es un sistema de información modular para el Centro de Estudiantes universitario. Está diseñado para centralizar la gestión de datos heterogéneos (finanzas, eventos, documentos, productos) bajo una única arquitectura flexible basada en MongoDB.

---

## Diagrama de capas

```
┌─────────────────────────────────────────────────────┐
│                    Frontend (React)                  │
│    Dashboard · Recursos · Finanzas · Eventos         │
└───────────────────────┬─────────────────────────────┘
                        │  HTTP / REST  (/api/v1)
┌───────────────────────▼─────────────────────────────┐
│                  Backend (FastAPI)                   │
│  ┌──────────┐ ┌──────────┐ ┌───────────┐ ┌───────┐  │
│  │ recursos │ │ finanzas │ │  eventos  │ │  ...  │  │
│  └────┬─────┘ └────┬─────┘ └─────┬─────┘ └───┬───┘  │
│       └────────────┴─────────────┴────────────┘      │
│                  recurso_service                     │
└───────────────────────┬─────────────────────────────┘
                        │  Motor (async)
┌───────────────────────▼─────────────────────────────┐
│               MongoDB Atlas                          │
│       Colección principal: recursos                  │
└─────────────────────────────────────────────────────┘
```

---

## Principios de diseño

### 1. Entidad unificada "Recurso"
Todos los módulos operan sobre la misma colección `recursos`. El campo `tipo` diferencia el módulo y `metadata` almacena la información específica de cada tipo, evitando la necesidad de múltiples colecciones o tablas.

### 2. Sin JOINs
Los datos relacionados (como el autor) se embeben directamente en el documento, eliminando la necesidad de consultas join complejas.

### 3. Schema flexible
El campo `metadata` no tiene esquema fijo, lo que permite añadir nuevos tipos de recursos sin migraciones de base de datos.

### 4. Separación de responsabilidades
- **Routers**: definen los endpoints HTTP (delgados, sin lógica de negocio)
- **Services**: contienen toda la lógica de negocio y acceso a datos
- **Schemas**: validan la entrada/salida de la API (Pydantic)
- **Models**: representan la estructura interna del documento MongoDB

---

## Flujo de una petición

```
Cliente HTTP
    ↓
Router (módulo/finanzas)
    ↓
Service (recurso_service.crear_recurso)
    ↓
Motor async → MongoDB Atlas
    ↓
Respuesta JSON validada por Pydantic
```

---

## Módulos funcionales

| Módulo | Tipo de Recurso | Endpoint base |
|---|---|---|
| Recursos (CRUD base) | cualquiera | `/api/v1/recursos` |
| Finanzas | `finanza` | `/api/v1/finanzas` |
| Eventos | `evento` | `/api/v1/eventos` |
| Repositorio | `documento` | `/api/v1/repositorio` |
| Dispensador | `producto` | `/api/v1/dispensador` |
