# Modelo de Datos — CEC Data Hub

## Colección principal: `recursos`

Todos los módulos del sistema almacenan sus datos en esta única colección. El campo `tipo` actúa como discriminador del módulo.

### Estructura base del documento

```json
{
  "_id": "ObjectId (generado automáticamente)",
  "tipo": "finanza | evento | documento | producto | otro",
  "titulo": "string",
  "descripcion": "string",
  "fecha": "ISODate",
  "autor": {
    "id": "string",
    "nombre": "string",
    "rol": "string"
  },
  "tags": ["string"],
  "metadata": { },
  "estado": "activo | inactivo | archivado"
}
```

> El campo `autor` está **embebido** para evitar JOINs. Si el usuario cambia de nombre, los documentos históricos conservan el nombre con que se crearon, lo que es el comportamiento correcto para auditoría.

---

## Ejemplos por tipo

### Finanza (ingreso/egreso)

```json
{
  "tipo": "finanza",
  "titulo": "Cuota socios — Mayo 2024",
  "fecha": "2024-05-01T00:00:00Z",
  "autor": { "id": "u001", "nombre": "Admin CEC", "rol": "admin" },
  "tags": ["cuota", "mensual"],
  "metadata": {
    "subtipo": "ingreso",
    "monto": 150000,
    "anio": 2024,
    "mes": 5,
    "comprobante": "https://drive.google.com/..."
  }
}
```

### Evento

```json
{
  "tipo": "evento",
  "titulo": "Semana de Integración 2024",
  "fecha": "2024-03-18T09:00:00Z",
  "autor": { "id": "u001", "nombre": "Admin CEC", "rol": "admin" },
  "tags": ["bienvenida", "primer_anio"],
  "metadata": {
    "lugar": "Patio central",
    "capacidad": 200,
    "asistentes": 175,
    "url_imagen": "https://..."
  }
}
```

### Documento académico

```json
{
  "tipo": "documento",
  "titulo": "Apuntes Cálculo I — 2023",
  "fecha": "2023-11-30T00:00:00Z",
  "autor": { "id": "u002", "nombre": "Juan P.", "rol": "vocal" },
  "tags": ["calculo", "matematicas"],
  "metadata": {
    "url": "https://drive.google.com/...",
    "tipo_archivo": "pdf",
    "asignatura": "Cálculo I",
    "carrera": "Ingeniería Civil"
  }
}
```

### Producto (máquina dispensadora)

```json
{
  "tipo": "producto",
  "titulo": "Agua mineral 500 ml",
  "autor": { "id": "u001", "nombre": "Admin CEC", "rol": "admin" },
  "tags": ["bebida"],
  "metadata": {
    "precio": 800,
    "stock": 15,
    "slot": "A1"
  }
}
```

---

## Colección `usuarios` (complementaria)

```json
{
  "_id": "ObjectId",
  "nombre": "Admin CEC",
  "email": "admin@cec.cl",
  "rol": "admin | tesorero | vocal | secretario"
}
```

---

## Índices recomendados

| Campo(s) | Justificación |
|---|---|
| `tipo` | Filtrado por módulo (consulta más frecuente) |
| `tags` | Búsqueda por tags (array index) |
| `(tipo, fecha)` | Paginación cronológica por módulo |
| `metadata.slot` | Búsqueda rápida de slot del dispensador |
