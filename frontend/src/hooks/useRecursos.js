/**
 * Hook genérico para cargar recursos con filtros opcionales.
 * Ejemplo de uso:
 *   const { data, loading, error, refetch } = useRecursos({ tipo: 'evento' })
 */
import { useState, useEffect, useCallback } from 'react'
import { fetchRecursos } from '../services/api'

export function useRecursos(filtros = {}) {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const key = JSON.stringify(filtros)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetchRecursos(filtros)
      setData(res.data)
    } catch (err) {
      setError(err)
    } finally {
      setLoading(false)
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key])

  useEffect(() => { load() }, [load])

  return { data, loading, error, refetch: load }
}
