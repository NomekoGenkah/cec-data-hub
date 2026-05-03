/*
 * dispensador.ino
 * ---------------
 * Código base para la máquina dispensadora del Centro de Estudiantes.
 *
 * Hardware requerido:
 *   - Arduino Uno / Mega
 *   - Módulo servo (o motor paso a paso) para cada slot
 *   - Módulo comunicación serie (USB / HC-05 Bluetooth)
 *
 * Protocolo de comunicación (serie 9600 baud):
 *   Comando de entrada: "DESPACHAR:<slot>\n"  ej: "DESPACHAR:A1\n"
 *   Respuesta:          "OK:<slot>\n"  o  "ERROR:<motivo>\n"
 */

#include <Servo.h>

// ── Configuración ─────────────────────────────────────────────────────────
#define NUM_SLOTS 4
#define SERIAL_BAUD 9600

// Pines de servo para cada slot (ajustar según cableado)
const int SERVO_PINS[NUM_SLOTS] = {3, 5, 6, 9};

// Nombres de los slots (deben coincidir con metadata.slot en MongoDB)
const char* SLOT_NAMES[NUM_SLOTS] = {"A1", "A2", "B1", "B2"};

Servo servos[NUM_SLOTS];

// ── Setup ─────────────────────────────────────────────────────────────────
void setup() {
  Serial.begin(SERIAL_BAUD);
  for (int i = 0; i < NUM_SLOTS; i++) {
    servos[i].attach(SERVO_PINS[i]);
    servos[i].write(0);  // posición inicial (cerrado)
  }
  Serial.println("DISPENSADOR LISTO");
}

// ── Loop ──────────────────────────────────────────────────────────────────
void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    procesarComando(cmd);
  }
}

// ── Funciones ─────────────────────────────────────────────────────────────

/**
 * Despacha el producto del slot indicado girando el servo 90°
 * y regresándolo a la posición inicial tras 500 ms.
 */
void despacharSlot(int idx) {
  servos[idx].write(90);  // abrir
  delay(500);
  servos[idx].write(0);   // cerrar
}

int buscarSlot(const String& nombre) {
  for (int i = 0; i < NUM_SLOTS; i++) {
    if (nombre == SLOT_NAMES[i]) return i;
  }
  return -1;
}

void procesarComando(const String& cmd) {
  if (cmd.startsWith("DESPACHAR:")) {
    String slot = cmd.substring(10);
    int idx = buscarSlot(slot);
    if (idx >= 0) {
      despacharSlot(idx);
      Serial.print("OK:");
      Serial.println(slot);
    } else {
      Serial.print("ERROR:slot_desconocido:");
      Serial.println(slot);
    }
  } else {
    Serial.println("ERROR:comando_invalido");
  }
}
