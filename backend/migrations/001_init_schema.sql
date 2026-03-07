-- AI日报 v2.0 数据库初始化脚本
-- 执行顺序: 先创建表，再插入基础数据

-- 1. 创建报告主表
CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    version VARCHAR(10) DEFAULT '2.0',
    headline_title VARCHAR(500),
    headline_content TEXT,
    headline_sources JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_reports_date ON reports(date);

-- 2. 创建新闻表
CREATE TABLE IF NOT EXISTS news (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES reports(id) ON DELETE CASCADE,
    category VARCHAR(50) NOT NULL,
    title VARCHAR(500) NOT NULL,
    summary TEXT,
    source VARCHAR(100),
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_news_report_id ON news(report_id);
CREATE INDEX IF NOT EXISTS idx_news_category ON news(category);

-- 3. 创建AI产业链公司基础表（先创建，因为其他表依赖它）
CREATE TABLE IF NOT EXISTS ai_companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    layer VARCHAR(50) NOT NULL,
    position VARCHAR(500),
    description TEXT,
    logo_url VARCHAR(500),
    website VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ai_companies_layer ON ai_companies(layer);
CREATE INDEX IF NOT EXISTS idx_ai_companies_code ON ai_companies(code);

-- 4. 创建股票价格表
CREATE TABLE IF NOT EXISTS stock_prices (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES reports(id) ON DELETE CASCADE,
    company_id INTEGER REFERENCES ai_companies(id),
    price DECIMAL(10, 2) NOT NULL,
    change DECIMAL(5, 2),
    change_percent DECIMAL(5, 2),
    currency VARCHAR(10) NOT NULL,
    volume BIGINT,
    market_cap BIGINT,
    recorded_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_stock_prices_report_id ON stock_prices(report_id);
CREATE INDEX IF NOT EXISTS idx_stock_prices_company_id ON stock_prices(company_id);

-- 5. 创建股票分析表
CREATE TABLE IF NOT EXISTS stock_analysis (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES reports(id) ON DELETE CASCADE,
    company_id INTEGER REFERENCES ai_companies(id),
    position VARCHAR(500),
    dynamics JSONB DEFAULT '[]',
    event VARCHAR(200),
    event_desc TEXT,
    risk TEXT,
    outlook TEXT,
    analysis_version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_stock_analysis_report_id ON stock_analysis(report_id);
CREATE INDEX IF NOT EXISTS idx_stock_analysis_company_id ON stock_analysis(company_id);

-- 6. 创建投资建议表
CREATE TABLE IF NOT EXISTS investment_advice (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES reports(id) ON DELETE CASCADE,
    short_term_title VARCHAR(200) DEFAULT '短期策略（1-3个月）',
    short_term_content TEXT,
    long_term_title VARCHAR(200) DEFAULT '中长期布局（6-12个月）',
    long_term_content TEXT,
    risk_title VARCHAR(200) DEFAULT '风险提示',
    risk_content TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_investment_advice_report_id ON investment_advice(report_id);

-- 7. 创建零售AI案例表
CREATE TABLE IF NOT EXISTS retail_cases (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES reports(id) ON DELETE CASCADE,
    company VARCHAR(100) NOT NULL,
    country VARCHAR(50),
    title VARCHAR(500) NOT NULL,
    summary TEXT,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_retail_cases_report_id ON retail_cases(report_id);

-- 插入AI产业链公司基础数据（15家）
INSERT INTO ai_companies (name, code, layer, position, description) VALUES
-- 基础设施层
('NVIDIA', 'NVDA', 'infrastructure', 'AI算力基础设施绝对龙头 | 数据中心收入占比 87%', '全球领先的GPU和AI芯片制造商'),
('AMD', 'AMD', 'infrastructure', 'NVIDIA最强挑战者 | MI300系列加速追赶', 'CPU和GPU双轮驱动的半导体公司'),
('Intel', 'INTC', 'infrastructure', 'CPU巨头转型AI | Gaudi系列加速卡', '全球最大的CPU制造商，积极布局AI芯片'),
('寒武纪', '688256.SH', 'infrastructure', '国产AI芯片龙头 | 思元系列云端训练/推理', '中国领先的AI芯片设计公司'),
('海光信息', '688041.SH', 'infrastructure', '国产CPU+DCU双轮驱动 | 深算系列AI芯片', '国产高性能处理器研发企业'),

-- 模型层
('OpenAI', '-', 'model', '大模型开创者 | GPT系列定义行业标准', 'ChatGPT和GPT系列模型开发商'),
('Alphabet', 'GOOGL', 'model', 'Google母公司 | Gemini与TPU生态', '拥有Google、DeepMind等AI研究团队'),
('Meta', 'META', 'model', '开源大模型领袖 | Llama生态', 'Facebook母公司，Llama开源模型'),
('阿里巴巴', 'BABA', 'model', '中国大模型第一梯队 | 通义千问', '通义千问大模型开发商'),
('科大讯飞', '002230.SZ', 'model', '国产大模型领军 | 星火认知大模型', '星火大模型和语音识别技术'),

-- 应用层
('Microsoft', 'MSFT', 'application', 'AI应用落地最快 | Copilot生态', 'Copilot和Azure OpenAI服务'),
('Adobe', 'ADBE', 'application', '创意AI领导者 | Firefly生态', 'Firefly生成式AI创意工具'),
('Salesforce', 'CRM', 'application', 'CRM+AI融合 | Einstein GPT', 'Einstein GPT企业AI助手'),
('Palantir', 'PLTR', 'application', '大数据+AI平台 | AIP军事/政府应用', 'AIP平台军事和商业AI应用'),
('Tesla', 'TSLA', 'application', '自动驾驶AI | FSD端到端神经网络', 'FSD自动驾驶和Dojo超算')

ON CONFLICT (code) DO NOTHING;

-- 验证数据插入
SELECT layer, COUNT(*) as count FROM ai_companies GROUP BY layer ORDER BY layer;
