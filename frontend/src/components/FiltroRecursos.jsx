/**
 * Fila de filtros para tipo y tags.
 * Props:
 *   tipo, setTipo     → valor y setter del filtro tipo
 *   tagInput, setTagInput, onAddTag, tags, onRemoveTag
 *   tipos             → array de opciones de tipo
 */
export default function FiltroRecursos({
  tipo,
  setTipo,
  tagInput,
  setTagInput,
  onAddTag,
  tags,
  onRemoveTag,
  tipos = ['finanza', 'evento', 'documento', 'producto'],
}) {
  return (
    <div className="flex flex-wrap gap-4 items-end mb-6">
      {/* Filtro tipo */}
      <div>
        <label className="block text-xs text-gray-500 mb-1">Tipo</label>
        <select
          value={tipo}
          onChange={(e) => setTipo(e.target.value)}
          className="border rounded px-3 py-1.5 text-sm"
        >
          <option value="">Todos</option>
          {tipos.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>
      </div>

      {/* Filtro tags */}
      <div>
        <label className="block text-xs text-gray-500 mb-1">Tags</label>
        <div className="flex gap-2">
          <input
            value={tagInput}
            onChange={(e) => setTagInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && onAddTag()}
            placeholder="Añadir tag…"
            className="border rounded px-3 py-1.5 text-sm w-36"
          />
          <button
            onClick={onAddTag}
            className="bg-cec-primary text-white text-sm px-3 rounded"
          >
            +
          </button>
        </div>
        <div className="flex gap-1 mt-1 flex-wrap">
          {tags.map((t) => (
            <span
              key={t}
              className="bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded-full flex items-center gap-1"
            >
              {t}
              <button onClick={() => onRemoveTag(t)} className="hover:text-red-500">
                ×
              </button>
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}
