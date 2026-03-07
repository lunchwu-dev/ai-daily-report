import type { InvestmentAdvice as InvestmentType } from '../types'

interface InvestmentSectionProps {
  investment: InvestmentType
}

export function InvestmentSection({ investment }: InvestmentSectionProps) {
  return (
    <section className="card">
      <h3 className="section-title bg-emerald-500/20 text-emerald-400 mb-6">
        💼 投资配置建议
      </h3>
      
      <div className="space-y-6">
        <div className="p-4 bg-emerald-500/10 rounded-xl border border-emerald-500/20">
          <h4 className="font-semibold text-emerald-400 mb-2">{investment.short_term_title}</h4>
          <p className="text-slate-300 leading-relaxed">{investment.short_term_content}</p>
        </div>
        
        <div className="p-4 bg-blue-500/10 rounded-xl border border-blue-500/20">
          <h4 className="font-semibold text-blue-400 mb-2">{investment.long_term_title}</h4>
          <p className="text-slate-300 leading-relaxed">{investment.long_term_content}</p>
        </div>
        
        <div className="p-4 bg-rose-500/10 rounded-xl border border-rose-500/20">
          <h4 className="font-semibold text-rose-400 mb-2">{investment.risk_title}</h4>
          <p className="text-slate-400 text-sm leading-relaxed">{investment.risk_content}</p>
        </div>
      </div>
    </section>
  )
}
