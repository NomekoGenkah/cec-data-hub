# Módulo Dispensador — Hardware

## Descripción

Código Arduino para controlar la máquina dispensadora de productos del Centro de Estudiantes.

## Requisitos de hardware

| Componente | Descripción |
|---|---|
| Arduino Uno / Mega | Microcontrolador principal |
| Servo SG90 (x4) | Un servo por slot de producto |
| Cable USB | Comunicación serie con el servidor |

## Protocolo serie (9600 baud)

| Dirección | Formato | Ejemplo |
|---|---|---|
| PC → Arduino | `DESPACHAR:<slot>\n` | `DESPACHAR:A1\n` |
| Arduino → PC | `OK:<slot>\n` | `OK:A1\n` |
| Arduino → PC | `ERROR:<motivo>\n` | `ERROR:slot_desconocido:Z9\n` |

## Slots disponibles

- **A1**, **A2**, **B1**, **B2** (4 slots por defecto, configurables en el .ino)

## Integración con el backend

El módulo `dispensador` de FastAPI envía el comando serie al Arduino cuando se registra un despacho, y actualiza el `stock` del producto en MongoDB.
