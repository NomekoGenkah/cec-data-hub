# Comparación SQL vs NoSQL — CEC Data Hub

Este documento analiza las decisiones de diseño del sistema, comparando el enfoque NoSQL (MongoDB) elegido con el equivalente relacional (SQL).

---

## 1. Modelo de datos

### SQL (relacional)

```sql
-- Se necesitan tablas separadas para cada tipo de recurso
CREATE TABLE recursos (
    id         SERIAL PRIMARY KEY,
    tipo       VARCHAR(50),
    titulo     VARCHAR(255),
    descripcion TEXT,
    fecha      TIMESTAMP,
    estado     VARCHAR(20),
    autor_id   INT REFERENCES usuarios(id)  -- FK
);

CREATE TABLE finanzas (
    id          SERIAL PRIMARY KEY,
    recurso_id  INT REFERENCES recursos(id),  -- FK
    subtipo     VARCHAR(20),
    monto       NUMERIC,
    anio        INT,
    mes         INT,
    comprobante VARCHAR(500)
);

CREATE TABLE eventos (
    id          SERIAL PRIMARY KEY,
    recurso_id  INT REFERENCES recursos(id),
    lugar       VARCHAR(255),
    capacidad   INT,
    asistentes  INT
);

CREATE TABLE recurso_tags (
    recurso_id INT REFERENCES recursos(id),
    tag        VARCHAR(100),
    PRIMARY KEY (recurso_id, tag)
);
```

### NoSQL (MongoDB)

```json
{
  "_id": "ObjectId",
  "tipo": "finanza",
  "titulo": "Cuota mayo",
  "autor": { "id": "u1", "nombre": "Admin", "rol": "admin" },
  "tags": ["cuota"],
  "metadata": { "subtipo": "ingreso", "monto": 150000, "anio": 2024, "mes": 5 }
}
```

**Diferencia clave**: MongoDB usa un único documento con `metadata` flexible; SQL requiere múltiples tablas y JOINs.

---

## 2. Consultas comparadas

### Listar eventos con su autor

#### SQL
```sql
SELECT r.titulo, r.fecha, u.nombre AS autor, e.lugar, e.capacidad
FROM recursos r
JOIN usuarios u ON r.autor_id = u.id
JOIN eventos e ON e.recurso_id = r.id
WHERE r.tipo = 'evento';
```

#### MongoDB
```python
# Sin JOIN: el autor ya está embebido en el documento
db.recursos.find({"tipo": "evento"})
```

---

### Suma de ingresos por mes

#### SQL
```sql
SELECT EXTRACT(YEAR FROM r.fecha)  AS anio,
       EXTRACT(MONTH FROM r.fecha) AS mes,
       SUM(f.monto)                AS total
FROM recursos r
JOIN finanzas f ON f.recurso_id = r.id
WHERE f.subtipo = 'ingreso'
GROUP BY anio, mes
ORDER BY anio, mes;
```

#### MongoDB (pipeline de agregación)
```python
db.recursos.aggregate([
    {"$match": {"tipo": "finanza", "metadata.subtipo": "ingreso"}},
    {"$group": {
        "_id": {"anio": "$metadata.anio", "mes": "$metadata.mes"},
        "total": {"$sum": "$metadata.monto"}
    }},
    {"$sort": {"_id.anio": 1, "_id.mes": 1}}
])
```

---

### Buscar por tag

#### SQL
```sql
SELECT r.*
FROM recursos r
JOIN recurso_tags t ON t.recurso_id = r.id
WHERE t.tag = 'becas';
```

#### MongoDB
```python
# Los tags son un array en el mismo documento
db.recursos.find({"tags": "becas"})
```

---

## 3. Tabla comparativa

| Aspecto | SQL | MongoDB |
|---|---|---|
| Estructura | Tablas fijas con esquema rígido | Documentos flexibles |
| Relaciones | JOINs entre tablas | Datos embebidos o referencias |
| Agregar campo nuevo | `ALTER TABLE` (migración) | Sin migración, solo añadir campo |
| Consultas por tipo | Requiere JOIN | Filtro directo `{tipo: "..."}` |
| Búsqueda en arrays | Tabla intermedia + JOIN | Índice de array nativo |
| Escalabilidad horizontal | Compleja (sharding manual) | Nativa en MongoDB Atlas |
| Transacciones ACID | Soporte completo | Soporte multi-documento desde 4.0 |
| Curva de aprendizaje | Alta (normalización, JOINs) | Baja para estructuras anidadas |

---

## 4. ¿Cuándo preferir SQL?

- Datos altamente relacionales con muchas relaciones many-to-many
- Necesidad estricta de integridad referencial
- Reportes complejos con múltiples JOINs y agregaciones entre entidades distintas

## 5. ¿Por qué MongoDB para este sistema?

- Los módulos son **extensiones lógicas** del mismo tipo de dato (Recurso)
- El campo `metadata` varía significativamente entre módulos (schema flexible)
- Las consultas frecuentes son por tipo, tags o fecha (índices simples)
- La arquitectura del Centro de Estudiantes evoluciona constantemente: agregar un nuevo módulo no requiere migraciones
