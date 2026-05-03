/**
 * Cliente HTTP centralizado que apunta al backend FastAPI.
 * Todos los módulos importan las funciones de aquí para evitar
 * duplicar la URL base o los headers.
 */
import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

// ── Recursos ──────────────────────────────────────────────────────────────
export const fetchRecursos = (params = {}) => api.get('/recursos', { params })
export const getRecurso = (id) => api.get(`/recursos/${id}`)
export const createRecurso = (data) => api.post('/recursos', data)
export const updateRecurso = (id, data) => api.patch(`/recursos/${id}`, data)
export const deleteRecurso = (id) => api.delete(`/recursos/${id}`)

// ── Finanzas ──────────────────────────────────────────────────────────────
export const fetchFinanzas = (params = {}) => api.get('/finanzas', { params })
export const fetchResumenFinanzas = (params = {}) =>
  api.get('/finanzas/resumen', { params })
export const createFinanza = (data) => api.post('/finanzas', data)

// ── Eventos ──────────────────────────────────────────────────────────────
export const fetchEventos = (params = {}) => api.get('/eventos', { params })
export const createEvento = (data) => api.post('/eventos', data)

// ── Repositorio ──────────────────────────────────────────────────────────
export const fetchDocumentos = (params = {}) =>
  api.get('/repositorio', { params })
export const createDocumento = (data) => api.post('/repositorio', data)

// ── Dispensador ──────────────────────────────────────────────────────────
export const fetchProductos = (params = {}) =>
  api.get('/dispensador/productos', { params })
export const createProducto = (data) => api.post('/dispensador/productos', data)
export const ajustarStock = (id, cantidad) =>
  api.patch(`/dispensador/productos/${id}/stock`, null, { params: { cantidad } })

export default api
