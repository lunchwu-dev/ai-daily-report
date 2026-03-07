import { Newspaper, Globe, ShoppingBag } from 'lucide-react'
import type { News } from '../types'

interface NewsSectionProps {
  domestic: News[]
  international: News[]
  retail: News[]
}

export function NewsSection({ domestic, international, retail }: NewsSectionProps) {
  const sections = [
    { key: 'domestic', title: '🇨🇳 国内AI热点', icon: Newspaper, data: domestic, color: 'text-rose-400', bg: 'bg-rose-500/20' },
    { key: 'international', title: '🌍 海外AI热点', icon: Globe, data: international, color: 'text-blue-400', bg: 'bg-blue-500/20' },
    { key: 'retail', title: '🛍️ 零售AI应用', icon: ShoppingBag, data: retail, color: 'text-purple-400', bg: 'bg-purple-500/20' },
  ]

  return (
    <section className="space-y-8">
      {sections.map(section => (
        <div key={section.key}>
          <h3 className={`section-title ${section.bg} ${section.color} mb-4`}>
            <section.icon className="w-5 h-5" />
            {section.title}
          </h3>
          
          <div className="grid gap-4">
            {section.data?.map(news => (
              <div key={news.id} className="card hover:border-slate-600 transition">
                <div className="flex items-start gap-3">
                  <span className="px-2 py-1 bg-slate-700 rounded text-xs text-slate-300 shrink-0">
                    {news.source}
                  </span>
                  <div>
                    <h4 className="font-semibold mb-1">{news.title}</h4>
                    {news.summary && (
                      <p className="text-slate-400 text-sm">{news.summary}</p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </section>
  )
}
