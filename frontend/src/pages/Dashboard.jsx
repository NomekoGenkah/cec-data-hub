/**
 * Dashboard — vista general del sistema.
 * Muestra contadores por tipo de recurso y accesos rápidos.
 */
import { useEffect, useState } from 'react'
import StatCard from '../components/StatCard'
import { fetchRecursos } from '../services/api'

const TIPOS = [
  { tipo: 'finanza',   label: 'Finanzas',   color: 'bg-green-50' },
  { tipo: 'evento',    label: 'Eventos',    color: 'bg-blue-50'  },
  { tipo: 'documento', label: 'Documentos', color: 'bg-yellow-50'},
  { tipo: 'producto',  label: 'Productos',  color: 'bg-purple-50'},
]

export default function Dashboard() {
  const [counts, setCounts] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all(
      TIPOS.map(({ tipo }) =>
        fetchRecursos({ tipo, limit: 1 })
          .then((r) => ({ tipo, count: r.data.length }))
          .catch(() => ({ tipo, count: '?' }))
      )
    ).then((results) => {
      setCounts(Object.fromEntries(results.map((r) => [r.tipo, r.count])))
      setLoading(false)
    })
  }, [])

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Dashboard — Centro de Estudiantes</h1>

      {loading ? (
        <p className="text-gray-400">Cargando estadísticas…</p>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {TIPOS.map(({ tipo, label, color }) => (
            <StatCard
              key={tipo}
              title={label}
              value={counts[tipo] ?? 0}
              color={color}
            />
          ))}
        </div>
      )}

      <section className="mt-10">
        <h2 className="text-lg font-semibold mb-3">Accesos rápidos</h2>
        <div className="flex flex-wrap gap-3">
          {[
            { href: '/recursos', label: 'Ver todos los recursos' },
            { href: '/finanzas', label: 'Gestión financiera' },
            { href: '/eventos',  label: 'Próximos eventos' },
          ].map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="bg-cec-primary text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700 transition"
            >
              {link.label}
            </a>
          ))}
        </div>
      </section>
    </div>
  )
}
