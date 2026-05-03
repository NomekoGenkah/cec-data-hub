/**
 * Página Recursos — listado general con filtros por tipo y tags.
 */
import { useState } from 'react'
import { useRecursos } from '../hooks/useRecursos'
import FiltroRecursos from '../components/FiltroRecursos'
import { colorByTipo, formatDate } from '../utils/formatters'

export default function Recursos() {
  const [tipo, setTipo]     = useState('')
  const [tags, setTags]     = useState([])
  const [tagInput, setTagInput] = useState('')

  const filtros = {}
  if (tipo) filtros.tipo = tipo
  if (tags.length) filtros.tags = tags

  const { data, loading, error } = useRecursos(filtros)

  const addTag = () => {
    const t = tagInput.trim()
    if (t && !tags.includes(t)) setTags([...tags, t])
    setTagInput('')
  }

  const removeTag = (t) => setTags(tags.filter((x) => x !== t))

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Recursos</h1>

      <FiltroRecursos
        tipo={tipo} setTipo={setTipo}
        tagInput={tagInput} setTagInput={setTagInput}
        onAddTag={addTag} tags={tags} onRemoveTag={removeTag}
      />

      {loading && <p className="text-gray-400">Cargando…</p>}
      {error   && <p className="text-red-500">Error al cargar recursos.</p>}

      <div className="space-y-3">
        {data.map((r) => (
          <div key={r.id} className="bg-white rounded-xl shadow p-4 flex gap-4 items-start">
            <span className={`text-xs px-2 py-0.5 rounded-full font-medium mt-0.5 ${colorByTipo(r.tipo)}`}>
              {r.tipo}
            </span>
            <div className="flex-1">
              <p className="font-semibold">{r.titulo}</p>
              <p className="text-sm text-gray-500">{r.descripcion}</p>
              <p className="text-xs text-gray-400 mt-1">{formatDate(r.fecha)}</p>
              {r.tags.length > 0 && (
                <div className="flex gap-1 mt-1 flex-wrap">
                  {r.tags.map((t) => (
                    <span key={t} className="bg-gray-100 text-gray-600 text-xs px-2 py-0.5 rounded-full">
                      {t}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {!loading && data.length === 0 && (
        <p className="text-gray-400 mt-4">No hay recursos con los filtros seleccionados.</p>
      )}
    </div>
  )
}
