import { ShoppingCart } from 'lucide-react'
import type { RetailCase } from '../types'

interface RetailCasesProps {
  cases: RetailCase[]
}

export function RetailCases({ cases }: RetailCasesProps) {
  return (
    <section className="card">
      <h3 className="section-title bg-purple-500/20 text-purple-400 mb-6">
        <ShoppingCart className="w-5 h-5" />
        零售AI应用实践
      </h3>

      <div className="grid gap-4">
        {cases?.map((item, index) => (
          <div key={index} className="p-4 bg-slate-800/50 rounded-xl border border-slate-700">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-lg">{item.country}</span>
              <span className="px-2 py-0.5 bg-purple-500/20 text-purple-400 rounded text-sm">
                {item.company}
              </span>
            </div>
            <h4 className="font-semibold mb-1">{item.title}</h4>
            {item.summary && (
              <p className="text-slate-400 text-sm">{item.summary}</p>
            )}
          </div>
        ))}
      </div>
    </section>
  )
}
