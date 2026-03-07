// 类型定义

export interface AICompany {
  id: number
  name: string
  code: string
  layer: 'infrastructure' | 'model' | 'application'
  position?: string
}

export interface News {
  id: number
  category: 'domestic' | 'international' | 'retail'
  title: string
  summary?: string
  source?: string
}

export interface StockPrice {
  id: number
  company_name: string
  company_code: string
  company_layer: string
  price: number
  change?: number
  change_percent?: number
  currency: string
}

export interface StockAnalysis {
  position?: string
  dynamics: string[]
  event?: string
  event_desc?: string
  risk?: string
  outlook?: string
}

export interface Stock extends StockPrice, StockAnalysis {}

export interface InvestmentAdvice {
  short_term_title: string
  short_term_content?: string
  long_term_title: string
  long_term_content?: string
  risk_title: string
  risk_content?: string
}

export interface RetailCase {
  company: string
  country?: string
  title: string
  summary?: string
}

export interface Headline {
  title?: string
  content?: string
  sources: { source: string; viewpoint: string }[]
}

export interface Report {
  id: number
  date: string
  version: string
  headline: Headline
  news: {
    domestic: News[]
    international: News[]
    retail: News[]
  }
  stocks: {
    infrastructure: Stock[]
    model: Stock[]
    application: Stock[]
  }
  investment: InvestmentAdvice
  retail_cases: RetailCase[]
}
