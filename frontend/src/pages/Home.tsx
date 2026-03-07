import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Calendar, ChevronRight } from 'lucide-react'
import { reportsApi } from '../services/api'
import type { Report } from '../types'

export function HomePage() {
  const [reports, setReports] = useState<Report[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    reportsApi.getList(0, 30)
      .then(res => setReports(res.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return <div className="text-center py-20">加载中...</div>
  }

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <section className="text-center py-16">
        <h2 className="text-4xl font-bold mb-4 gradient-text">
          AI产业视角 · 感知智能脉搏
        </h2>
        <p className="text-slate-400 text-lg max-w-2xl mx-auto">
          每日精选全球人工智能热点，深度分析AI产业链投资机会
        </p>
        
        <Link 
          to="/latest"
          className="inline-block mt-8 px-8 py-3 bg-indigo-600 hover:bg-indigo-700 rounded-xl font-medium transition"
        >
          查看最新报告
        </Link>
      </section>

      {/* 历史报告列表 */}
      <section>
        <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
          <Calendar className="w-5 h-5" />
          历史报告
        </h3>

        <div className="grid gap-4">
          {reports.map(report => (
            <Link
              key={report.id}
              to={`/report/${report.date}`}
              className="card hover:border-indigo-500 transition group"
            >
              <div className="flex items-center justify-between"
003e
                <div>
                  <div className="text-lg font-semibold group-hover:text-indigo-400 transition">
                    {report.date}
                  </div>
                  <p className="text-slate-400 text-sm mt-1 line-clamp-1">
                    {report.headline?.title || '暂无标题'}
                  </p>
                </div>
                <ChevronRight className="w-5 h-5 text-slate-500 group-hover:text-indigo-400" />
              </div>
            </Link>
          ))}
        </div>
      </section>
    </div>
  )
}
