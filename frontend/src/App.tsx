import { useEffect, useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import { Header } from './components/Header'
import { Footer } from './components/Footer'
import { HomePage } from './pages/Home'
import { ReportPage } from './pages/Report'
import { api } from './services/api'

function App() {
  const [apiStatus, setApiStatus] = useState<string>('checking')

  useEffect(() => {
    // 检查API状态
    api.get('/health')
      .then(() => setApiStatus('connected'))
      .catch(() => setApiStatus('disconnected'))
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-900 to-indigo-950">
      <Header apiStatus={apiStatus} />
      
      <main className="container mx-auto px-4 py-8 max-w-6xl">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/report/:date" element={<ReportPage />} />
          <Route path="/latest" element={<ReportPage />} />
        </Routes>
      </main>

      <Footer />
    </div>
  )
}

export default App
