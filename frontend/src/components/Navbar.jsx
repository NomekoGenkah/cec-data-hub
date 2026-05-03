import { Link, useLocation } from 'react-router-dom'

const links = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/recursos', label: 'Recursos' },
  { to: '/finanzas', label: 'Finanzas' },
  { to: '/eventos', label: 'Eventos' },
]

export default function Navbar() {
  const { pathname } = useLocation()

  return (
    <nav className="bg-cec-primary shadow">
      <div className="container mx-auto px-4 flex items-center gap-6 h-14">
        <span className="text-white font-bold text-lg tracking-tight">CEC Data Hub</span>
        {links.map((l) => (
          <Link
            key={l.to}
            to={l.to}
            className={`text-sm font-medium transition-colors ${
              pathname.startsWith(l.to)
                ? 'text-cec-accent'
                : 'text-blue-200 hover:text-white'
            }`}
          >
            {l.label}
          </Link>
        ))}
      </div>
    </nav>
  )
}
