import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v2'

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 报告相关API
export const reportsApi = {
  getLatest: () => api.get('/reports/latest'),
  getByDate: (date: string) => api.get(`/reports/${date}`),
  getList: (skip = 0, limit = 30) => api.get(`/reports?skip=${skip}&limit=${limit}`),
}

// 股票相关API
export const stocksApi = {
  getHistory: (code: string, start?: string, end?: string) => 
    api.get(`/stocks/${code}/history`, { params: { start, end } }),
  getLosers: () => api.get('/stocks/today/losers'),
  getGainers: () => api.get('/stocks/today/gainers'),
}

// 公司相关API
export const companiesApi = {
  getList: () => api.get('/companies'),
  getLayers: () => api.get('/companies/layers'),
}
