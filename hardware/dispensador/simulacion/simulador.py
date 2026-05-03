"""
simulador.py
------------
Simula el comportamiento del Arduino para desarrollo sin hardware real.
Abre un puerto serie virtual y responde al protocolo DESPACHAR:<slot>.

Uso:
    python simulador.py [--port /dev/ttyUSB0] [--baud 9600]

Dependencias:
    pip install pyserial
"""
import argparse
import time
import sys

# Intenta importar pyserial; si no está disponible, usa modo demo
try:
    import serial
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False

SLOTS_VALIDOS = {"A1", "A2", "B1", "B2"}


def despachar(slot: str) -> str:
    """Simula el accionamiento mecánico del slot."""
    if slot not in SLOTS_VALIDOS:
        return f"ERROR:slot_desconocido:{slot}"
    print(f"  [SIM] Abriendo servo del slot {slot}…", flush=True)
    time.sleep(0.5)
    print(f"  [SIM] Cerrando servo del slot {slot}.", flush=True)
    return f"OK:{slot}"


def procesar_comando(cmd: str) -> str:
    cmd = cmd.strip()
    if cmd.startswith("DESPACHAR:"):
        slot = cmd[len("DESPACHAR:"):]
        return despachar(slot)
    return "ERROR:comando_invalido"


# ── Modo demo (sin puerto serie real) ─────────────────────────────────────
def modo_demo():
    print("=== Simulador Dispensador (modo demo — sin puerto serie) ===")
    print("Escribe un comando como: DESPACHAR:A1")
    print("Ctrl+C para salir\n")
    while True:
        try:
            cmd = input("CMD> ")
            resp = procesar_comando(cmd)
            print(f"  → {resp}\n")
        except KeyboardInterrupt:
            print("\nSimulador detenido.")
            sys.exit(0)


# ── Modo serie real ────────────────────────────────────────────────────────
def modo_serie(port: str, baud: int):
    print(f"=== Simulador Dispensador en {port} @ {baud} baud ===")
    with serial.Serial(port, baud, timeout=1) as ser:
        ser.write(b"DISPENSADOR LISTO\n")
        while True:
            line = ser.readline().decode("utf-8", errors="ignore")
            if line:
                resp = procesar_comando(line)
                print(f"RX: {line.strip()}  →  TX: {resp}")
                ser.write((resp + "\n").encode())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulador de dispensadora CEC")
    parser.add_argument("--port", default=None, help="Puerto serie (ej: /dev/ttyUSB0)")
    parser.add_argument("--baud", type=int, default=9600)
    args = parser.parse_args()

    if args.port and SERIAL_AVAILABLE:
        modo_serie(args.port, args.baud)
    else:
        modo_demo()
