import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, TrendingUp, TrendingDown } from 'lucide-react'
import { reportsApi } from '../services/api'
import type { Report, Stock } from '../types'

export function ReportPage() {
  const { date } = useParams()
  const navigate = useNavigate()
  const [report, setReport] = useState<Report | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const api = date ? reportsApi.getByDate(date) : reportsApi.getLatest()
        const res = await api
        setReport(res.data)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetchReport()
  }, [date])

  if (loading) return <div className="text-center py-20">加载中...</div>
  if (!report) return <div className="text-center py-20">报告未找到</div>

  return (
    <div className="space-y-8">
      {/* 返回按钮 */}
      <button 
        onClick={() => navigate(-1)}
        className="flex items-center gap-2 text-slate-400 hover:text-white transition"
      >
        <ArrowLeft className="w-4 h-4" /> 返回
      </button>

      {/* 报告标题 */}
      <header className="text-center py-8">
        <div className="text-sm text-slate-400 mb-2">{report.date}</div>
        <h1 className="text-2xl font-bold gradient-text">AI日报</h1>
      </header>

      {/* 今日头条 */}
      {report.headline?.title && (
        <section className="card border-l-4 border-amber-500">
          <div className="flex items-center gap-2 mb-4">
            <span className="px-3 py-1 bg-amber-500 text-slate-900 rounded-full text-sm font-bold">
              今日头条
            </span>
          </div>
          <h2 className="text-xl font-bold text-amber-400 mb-3">{report.headline.title}</h2>
          <p className="text-slate-300 leading-relaxed">{report.headline.content}</p>
        </section>
      )}

      {/* 股票板块 */}
      <section>
        <h3 className="section-title bg-amber-500/20 text-amber-400 mb-6">
          📈 AI产业股票分析
        </h3>

        {['infrastructure', 'model', 'application'].map(layer => {
          const layerNames = {
            infrastructure: '🏗️ 基础设施层',
            model: '🧠 模型层',
            application: '💡 应用层'
          }
          const stocks = report.stocks?.[layer as keyof typeof report.stocks] || []
          
          return (
            <div key={layer} className="mb-8">
              <h4 className="text-lg font-semibold mb-4 text-indigo-400">{layerNames[layer as keyof typeof layerNames]}</h4>
              <div className="grid gap-4">
                {stocks.map((stock: Stock) => (
                  <div key={stock.id} className="card">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <div className="font-bold">{stock.company_name} ({stock.company_code})</div>
                        <div className="text-sm text-slate-400">{stock.position}</div>
                      </div>
                      <div className="text-right">
                        <div className="text-xl font-bold">{stock.price} {stock.currency}</div>
                        <div className={`flex items-center gap-1 ${(stock.change_percent || 0) >= 0 ? 'text-emerald-500' : 'text-rose-500'}`}>
                          {(stock.change_percent || 0) >= 0 ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                          <span>{stock.change_percent > 0 ? '+' : ''}{stock.change_percent}%</span>
                        </div>
                      </div>
                    </div>
                    
                    {stock.event && (
                      <div className="mt-4 pt-4 border-t border-slate-700">
                        <div className="text-sm">
                          <span className="text-amber-400 font-medium">{stock.event}</span>
                          <span className="text-slate-400 ml-2">{stock.event_desc}</span>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )
        })}
      </section>

      {/* 投资建议 */}
      {report.investment && (
        <section className="card">
          <h3 className="section-title bg-emerald-500/20 text-emerald-400 mb-6">
            💼 投资配置建议
          </h3>
          
          <div className="space-y-6">
            <div>
              <h4 className="font-semibold text-emerald-400 mb-2">{report.investment.short_term_title}</h4>
              <p className="text-slate-300">{report.investment.short_term_content}</p>
            </div>
            
            <div>
              <h4 className="font-semibold text-emerald-400 mb-2">{report.investment.long_term_title}</h4>
              <p className="text-slate-300">{report.investment.long_term_content}</p>
            </div>
            
            <div className="pt-4 border-t border-slate-700">
              <h4 className="font-semibold text-rose-400 mb-2">{report.investment.risk_title}</h4>
              <p className="text-slate-400 text-sm">{report.investment.risk_content}</p>
            </div>
          </div>
        </section>
      )}
    </div>
  )
}
