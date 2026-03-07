import { Link } from 'react-router-dom'
import { TrendingUp, Wifi, WifiOff } from 'lucide-react'

interface HeaderProps {
  apiStatus: string
}

export function Header({ apiStatus }: HeaderProps) {
  return (
    <header className="bg-slate-800/50 backdrop-blur-lg border-b border-slate-700 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4 max-w-6xl">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-3">
            <TrendingUp className="w-8 h-8 text-indigo-500" />
            <div>
              <h1 className="text-xl font-bold gradient-text">
                AI日报
              </h1>
              <p className="text-xs text-slate-400">IT小路的每日AI简报</p>
            </div>
          </Link>

          <div className="flex items-center gap-4">
            {/* API状态指示器 */}
            <div className="flex items-center gap-2 text-sm">
              {apiStatus === 'connected' ? (
                <>
                  <Wifi className="w-4 h-4 text-emerald-500" />
                  <span className="text-emerald-500">已连接</span>
                </>
              ) : apiStatus === 'disconnected' ? (
                <>
                  <WifiOff className="w-4 h-4 text-rose-500" />
                  <span className="text-rose-500">未连接</span>
                </>
              ) : (
                <span className="text-slate-400">检查中...</span>
              )}
            </div>

            <Link 
              to="/latest" 
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-lg text-sm font-medium transition"
            >
              最新报告
            </Link>
          </div>
        </div>
      </div>
    </header>
  )
}
