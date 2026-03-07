import { Layers } from 'lucide-react'
import type { AICompany } from '../types'

interface AIChainMapProps {
  companies: AICompany[]
}

export function AIChainMap({ companies }: AIChainMapProps) {
  const layers = [
    { key: 'infrastructure', title: '🏗️ 基础设施层', color: 'text-emerald-400', bg: 'bg-emerald-500/20' },
    { key: 'model', title: '🧠 模型层', color: 'text-violet-400', bg: 'bg-violet-500/20' },
    { key: 'application', title: '💡 应用层', color: 'text-cyan-400', bg: 'bg-cyan-500/20' },
  ]

  return (
    <section className="card">
      <h3 className="section-title bg-slate-700 text-slate-200 mb-6">
        <Layers className="w-5 h-5" />
        AI产业链全景
      </h3>

      <div className="space-y-6">
        {layers.map(layer => {
          const layerCompanies = companies.filter(c => c.layer === layer.key)
          
          return (
            <div key={layer.key} className="p-4 bg-slate-800/50 rounded-xl">
              <h4 className={`font-semibold mb-3 ${layer.color}`}>{layer.title}</h4>
              <div className="flex flex-wrap gap-2">
                {layerCompanies.map(company => (
                  <div
                    key={company.id}
                    className={`px-3 py-2 ${layer.bg} rounded-lg text-sm border border-slate-700`}
                  >
                    <div className="font-medium">{company.name}</div>
                    <div className="text-xs text-slate-400">{company.code}</div>
                  </div>
                ))}
              </div>
            </div>
          )
        })}
      </div>
    </section>
  )
}
