/**
 * Página Eventos — lista los próximos eventos del centro de estudiantes.
 */
import { useEffect, useState } from 'react'
import { fetchEventos } from '../services/api'
import { formatDate } from '../utils/formatters'

export default function Eventos() {
  const [eventos, setEventos] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchEventos().then((res) => {
      setEventos(res.data)
      setLoading(false)
    })
  }, [])

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Eventos</h1>

      {loading && <p className="text-gray-400">Cargando…</p>}

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {eventos.map((e) => (
          <div key={e.id} className="bg-white rounded-xl shadow overflow-hidden">
            {e.metadata?.url_imagen && (
              <img
                src={e.metadata.url_imagen}
                alt={e.titulo}
                className="w-full h-36 object-cover"
              />
            )}
            <div className="p-4">
              <p className="font-semibold text-lg">{e.titulo}</p>
              <p className="text-sm text-gray-500 mt-1">{e.descripcion}</p>
              <div className="flex justify-between items-center mt-3 text-xs text-gray-400">
                <span>{formatDate(e.fecha)}</span>
                {e.metadata?.lugar && (
                  <span className="bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full">
                    {e.metadata.lugar}
                  </span>
                )}
              </div>
              {e.metadata?.capacidad != null && (
                <div className="mt-2 text-xs text-gray-500">
                  Asistentes: {e.metadata.asistentes ?? 0} / {e.metadata.capacidad}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {!loading && eventos.length === 0 && (
        <p className="text-gray-400 mt-4">No hay eventos registrados.</p>
      )}
    </div>
  )
}
