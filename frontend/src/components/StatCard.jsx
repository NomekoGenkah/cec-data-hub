/**
 * Tarjeta reutilizable con título, valor y color de fondo opcional.
 */
export default function StatCard({ title, value, color = 'bg-white' }) {
  return (
    <div className={`rounded-xl shadow p-6 ${color}`}>
      <p className="text-sm text-gray-500 uppercase tracking-wide">{title}</p>
      <p className="text-3xl font-bold mt-1">{value}</p>
    </div>
  )
}
