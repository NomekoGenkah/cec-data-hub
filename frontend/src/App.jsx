import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Recursos from './pages/Recursos'
import Finanzas from './pages/Finanzas'
import Eventos from './pages/Eventos'
import Navbar from './components/Navbar'

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50 text-gray-900">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/recursos" element={<Recursos />} />
            <Route path="/finanzas" element={<Finanzas />} />
            <Route path="/eventos" element={<Eventos />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
