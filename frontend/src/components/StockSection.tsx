import { TrendingUp, TrendingDown } from 'lucide-react'
import type { Stock } from '../types'

interface StockSectionProps {
  stocks?: {
    infrastructure: Stock[]
    model: Stock[]
    application: Stock[]
  }
}

export function StockSection({ stocks }: StockSectionProps) {
  const layers = [
    { key: 'infrastructure', title: '🏗️ 基础设施层', color: 'text-emerald-400' },
    { key: 'model', title: '🧠 模型层', color: 'text-violet-400' },
    { key: 'application', title: '💡 应用层', color: 'text-cyan-400' },
  ] as const

  return (
    <section>
      <h3 className="section-title bg-amber-500/20 text-amber-400 mb-6">
        📈 AI产业股票分析
      </h3>

      {layers.map(layer => {
        const layerStocks = stocks?.[layer.key] || []
        
        return (
          <div key={layer.key} className="mb-8">
            <h4 className={`text-lg font-semibold mb-4 ${layer.color}`}>{layer.title}</h4>
            <div className="grid gap-4">
              {layerStocks.map((stock: Stock) => (
                <div key={stock.id} className="card">
                  <div className="flex items-center justify-between mb-3">
                    <div>
                      <div className="font-bold">{stock.company_name} ({stock.company_code})</div>
                      <div className="text-sm text-slate-400">{stock.position}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-xl font-bold">{stock.price} {stock.currency}</div>
                      <div className={`flex items-center gap-1 justify-end ${(stock.change_percent || 0) >= 0 ? 'text-emerald-500' : 'text-rose-500'}`}>
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
  )
}
