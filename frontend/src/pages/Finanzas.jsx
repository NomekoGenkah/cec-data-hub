/**
 * Página Finanzas — lista transacciones y muestra resumen por mes.
 */
import { useEffect, useState } from 'react'
import { fetchFinanzas, fetchResumenFinanzas } from '../services/api'
import { formatCLP, formatDate } from '../utils/formatters'

export default function Finanzas() {
  const [finanzas, setFinanzas]   = useState([])
  const [resumen,  setResumen]    = useState([])
  const [loading,  setLoading]    = useState(true)

  useEffect(() => {
    Promise.all([fetchFinanzas(), fetchResumenFinanzas()]).then(
      ([fRes, rRes]) => {
        setFinanzas(fRes.data)
        setResumen(rRes.data)
        setLoading(false)
      }
    )
  }, [])

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Finanzas</h1>

      {loading && <p className="text-gray-400">Cargando…</p>}

      {!loading && (
        <>
          {/* Resumen por mes */}
          {resumen.length > 0 && (
            <section className="mb-8">
              <h2 className="text-lg font-semibold mb-3">Resumen por mes</h2>
              <div className="overflow-x-auto">
                <table className="w-full text-sm border-collapse">
                  <thead>
                    <tr className="bg-gray-100">
                      <th className="text-left p-2 border">Año</th>
                      <th className="text-left p-2 border">Mes</th>
                      <th className="text-left p-2 border">Subtipo</th>
                      <th className="text-right p-2 border">Total</th>
                      <th className="text-right p-2 border">N°</th>
                    </tr>
                  </thead>
                  <tbody>
                    {resumen.map((r, i) => (
                      <tr key={i} className="hover:bg-gray-50">
                        <td className="p-2 border">{r._id?.anio ?? '—'}</td>
                        <td className="p-2 border">{r._id?.mes ?? '—'}</td>
                        <td className="p-2 border">{r._id?.subtipo ?? '—'}</td>
                        <td className="p-2 border text-right font-mono">
                          {formatCLP(r.total)}
                        </td>
                        <td className="p-2 border text-right">{r.cantidad}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          )}

          {/* Listado de transacciones */}
          <h2 className="text-lg font-semibold mb-3">Transacciones</h2>
          <div className="space-y-2">
            {finanzas.map((f) => (
              <div key={f.id} className="bg-white rounded-xl shadow p-4 flex justify-between items-center">
                <div>
                  <p className="font-medium">{f.titulo}</p>
                  <p className="text-xs text-gray-400">{formatDate(f.fecha)}</p>
                </div>
                <span
                  className={`font-bold font-mono ${
                    f.metadata?.subtipo === 'ingreso' ? 'text-green-600' : 'text-red-500'
                  }`}
                >
                  {f.metadata?.subtipo === 'ingreso' ? '+' : '-'}
                  {formatCLP(f.metadata?.monto ?? 0)}
                </span>
              </div>
            ))}
          </div>

          {finanzas.length === 0 && (
            <p className="text-gray-400 mt-4">No hay transacciones registradas.</p>
          )}
        </>
      )}
    </div>
  )
}
