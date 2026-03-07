import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { reportsApi, companiesApi } from '../services/api'
import { NewsSection } from '../components/NewsSection'
import { AIChainMap } from '../components/AIChainMap'
import { RetailCases } from '../components/RetailCases'
import { StockSection } from '../components/StockSection'
import { InvestmentSection } from '../components/InvestmentSection'
import type { Report, AICompany } from '../types'

export function ReportPage() {
  const { date } = useParams()
  const navigate = useNavigate()
  const [report, setReport] = useState<Report | null>(null)
  const [companies, setCompanies] = useState<AICompany[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [reportRes, companiesRes] = await Promise.all([
          date ? reportsApi.getByDate(date) : reportsApi.getLatest(),
          companiesApi.getList()
        ])
        setReport(reportRes.data)
        setCompanies(companiesRes.data)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
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

      {/* 新闻板块 */}
      <NewsSection 
        domestic={report.news?.domestic || []}
        international={report.news?.international || []}
        retail={report.news?.retail || []}
      />

      {/* AI产业链全景 */}
      <AIChainMap companies={companies} />

      {/* 股票板块 */}
      <StockSection stocks={report.stocks} />

      {/* 零售AI案例 */}
      <RetailCases cases={report.retail_cases} />

      {/* 投资建议 */}
      {report.investment && <InvestmentSection investment={report.investment} />}
    </div>
  )
}
