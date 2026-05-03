/**
 * Utilidades de formato para la UI.
 */

/** Formatea un número como moneda chilena (CLP). */
export function formatCLP(amount) {
  return new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP',
    maximumFractionDigits: 0,
  }).format(amount)
}

/** Formatea una fecha ISO como string legible en español. */
export function formatDate(isoString) {
  return new Date(isoString).toLocaleDateString('es-CL', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  })
}

/** Devuelve un color Tailwind según el tipo de recurso. */
export function colorByTipo(tipo) {
  const map = {
    finanza: 'bg-green-100 text-green-800',
    evento: 'bg-blue-100 text-blue-800',
    documento: 'bg-yellow-100 text-yellow-800',
    producto: 'bg-purple-100 text-purple-800',
  }
  return map[tipo] ?? 'bg-gray-100 text-gray-800'
}
