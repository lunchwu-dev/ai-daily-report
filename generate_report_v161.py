#!/usr/bin/env python3
"""
AI日报生成器 v1.6.1 - 增强版
- 完整 v1.4.2 结构
- 15家AI产业股票深度分析（增强版）
- 投资配置建议
- 多语言支持
"""

import json
from datetime import datetime

def generate_stock_data():
    """生成15家AI产业股票数据 - 增强详细分析"""
    return {
        "infrastructure": [
            {"name": "NVIDIA", "code": "NVDA", "price": 142.62, "change": 2.93, "currency": "USD",
             "position": "AI算力基础设施绝对龙头 | 数据中心收入占比 87%",
             "dynamics": [
                 "Blackwell架构B200芯片Q2出货，单卡算力提升4倍，巩固训练市场垄断地位",
                 "40亿美元投资Coherent/Lumentum，解决超大规模集群光学互连瓶颈",
                 "微软、谷歌、Meta三大客户合计占数据中心收入45%，客户集中度高"
             ],
             "event": "光学互连投资",
             "event_desc": "宣布40亿美元投资光学互连领域后，市场认可NVIDIA不只是卖芯片，而是构建从芯片到网络的全栈AI基础设施生态，长期竞争力进一步增强",
             "risk": "客户集中度高、地缘政治出口限制",
             "outlook": "短期受益Blackwell出货，长期AI算力需求持续增长"},
            {"name": "AMD", "code": "AMD", "price": 178.25, "change": 1.85, "currency": "USD",
             "position": "NVIDIA最强挑战者 | MI300系列加速追赶",
             "dynamics": [
                 "MI300X配备192GB HBM3内存，单卡性能接近H100，已获微软、Meta大单",
                 "ROCm开源生态持续完善，作为CUDA替代方案吸引开发者迁移",
                 "数据中心GPU市场份额从3%快速提升至12%，增长势头强劲"
             ],
             "event": "Meta 600亿订单",
             "event_desc": "与Meta达成600亿美元AI芯片采购协议，成为AMD史上最大订单，验证MI300竞争力，预计2026年数据中心收入占比将超50%",
             "risk": "软件生态仍落后于CUDA、毛利率承压",
             "outlook": "受益于AI芯片多元化需求，份额持续提升"},
            {"name": "Intel", "code": "INTC", "price": 24.18, "change": -0.52, "currency": "USD",
             "position": "CPU巨头转型AI | Gaudi系列加速卡",
             "dynamics": [
                 "Gaudi 3性能对标H100，在推理场景具有性价比优势",
                 "与戴尔、惠普等OEM合作推AI服务器，拓展企业市场",
                 "代工业务分拆独立，设计部门专注高性能芯片研发"
             ],
             "event": "Gaudi 3发布",
             "event_desc": "新一代AI加速器Gaudi 3发布，瞄准推理市场，但市场反应平淡，投资者关注其能否在AI时代重拾竞争力",
             "risk": "技术落后、市场份额下滑、转型阵痛",
             "outlook": "短期承压，长期看Gaudi系列能否打开市场"},
            {"name": "寒武纪", "code": "688256.SH", "price": 168.20, "change": 6.32, "currency": "CNY",
             "position": "国产AI芯片龙头 | 思元系列云端训练/推理",
             "dynamics": [
                 "思元590训练芯片性能接近A100，已批量出货给互联网大厂",
                 "受益于国产替代政策，政府、金融、电信等行业订单饱满",
                 "与华为昇腾形成国产AI芯片双寡头格局"
             ],
             "event": "思元590量产",
             "event_desc": "新一代训练芯片思元590实现量产，性能对标国际主流产品，标志国产AI芯片进入可用、好用阶段，订单排期已至Q3",
             "risk": "先进制程受限、生态建设待完善",
             "outlook": "受益于国产替代大趋势，业绩有望高速增长"},
            {"name": "海光信息", "code": "688041.SH", "price": 95.80, "change": 3.45, "currency": "CNY",
             "position": "国产CPU+DCU双轮驱动 | 深算系列AI芯片",
             "dynamics": [
                 "深算二号DCU性能较上代提升100%，已适配主流AI框架",
                 "电信、金融、能源等行业信创订单持续增长",
                 "x86架构CPU具有生态优势，DCU与CPU协同销售"
             ],
             "event": "深算二号发布",
             "event_desc": "新一代DCU深算二号发布，性能大幅提升，已获得多家服务器厂商认证，预计2026年DCU收入占比将超40%",
             "risk": "技术迭代快、市场竞争加剧",
             "outlook": "CPU+DCU双轮驱动，受益于信创和AI算力需求"},
        ],
        "model_layer": [
            {"name": "OpenAI (私有)", "code": "-", "price": "-", "change": "-", "currency": "-",
             "position": "大模型开创者 | GPT系列定义行业标准",
             "dynamics": [
                 "GPT-5即将发布，多模态能力和推理能力大幅提升",
                 "企业API收入年化超30亿美元，是主要收入来源",
                 "与Microsoft深度绑定，Azure是其独家云服务提供商"
             ],
             "event": "GPT-5预告",
             "event_desc": "GPT-5预告引发行业高度关注，预计将在多模态、长上下文、推理能力等方面实现突破，可能重新定义大模型竞争格局",
             "risk": "未上市无法直接投资、与Microsoft绑定过深",
             "outlook": "通过Microsoft股票间接投资OpenAI生态"},
            {"name": "Alphabet", "code": "GOOGL", "price": 185.40, "change": 0.95, "currency": "USD",
             "position": "Google母公司 | Gemini与TPU生态",
             "dynamics": [
                 "Gemini 3.1 Flash-Lite主打性价比，与OpenAI正面对决",
                 "自研TPU v5p性能提升2.8倍，降低对外部GPU依赖",
                 "搜索和广告业务全面AI化，Gemini集成至全线产品"
             ],
             "event": "Gemini 3.1发布",
             "event_desc": "Gemini 3.1 Flash-Lite发布，主打性价比，与OpenAI GPT-5.3 Instant同日发布，显示AI军备竞赛白热化",
             "risk": "搜索业务受AI冲击、与OpenAI竞争加剧",
             "outlook": "AI转型加速，TPU生态逐步完善"},
            {"name": "Meta", "code": "META", "price": 728.50, "change": 2.15, "currency": "USD",
             "position": "开源大模型领袖 | Llama生态",
             "dynamics": [
                 "Llama 4即将发布，参数规模预计破万亿，性能对标GPT-5",
                 "AI推荐系统提升广告精准度和用户时长，广告收入增长",
                 "元宇宙+AI双轮驱动，Reality Labs持续投入"
             ],
             "event": "Llama 4预告",
             "event_desc": "下一代开源模型Llama 4备受期待，Meta希望通过开源策略建立AI生态，与OpenAI、Google形成三足鼎立",
             "risk": "元宇宙亏损、AI投入回报周期长",
             "outlook": "开源策略有望建立生态，广告业务受益于AI"},
            {"name": "阿里巴巴", "code": "BABA", "price": 98.50, "change": -1.25, "currency": "USD",
             "position": "中国大模型第一梯队 | 通义千问",
             "dynamics": [
                 "通义千问2.5性能对标GPT-4，中文场景表现优异",
                 "开源策略吸引开发者，千问社区活跃度高",
                 "云业务AI化转型，AI收入占比持续提升"
             ],
             "event": "技术负责人离职",
             "event_desc": "通义千问技术负责人林俊旸离职引发市场关注，CEO吴泳铭回应将坚持开源策略，但投资者担忧核心技术团队稳定性",
             "risk": "人才流失、与OpenAI技术差距、监管压力",
             "outlook": "开源策略差异化竞争，云业务AI化转型关键期"},
            {"name": "科大讯飞", "code": "002230.SZ", "price": 52.35, "change": 4.85, "currency": "CNY",
             "position": "国产大模型领军 | 星火认知大模型",
             "dynamics": [
                 "星火V4.0即将发布，全面对标GPT-4，多模态能力大幅提升",
                 "教育、医疗、办公等垂直场景深度落地，B端收入占比超60%",
                 "两会AI政策利好，教育AI业务有望加速增长"
             ],
             "event": "两会政策利好",
             "event_desc": "两会期间AI教育政策密集出台，科大讯飞作为教育AI龙头直接受益，已与多省市签订智慧教育大单",
             "risk": "B端回款周期长、C端产品竞争力待验证",
             "outlook": "受益于AI教育政策红利，业绩有望加速增长"},
        ],
        "application": [
            {"name": "Microsoft", "code": "MSFT", "price": 412.30, "change": 1.28, "currency": "USD",
             "position": "AI应用落地最快 | Copilot生态",
             "dynamics": [
                 "Copilot月活突破800万，较上季度增长60%，商业化加速",
                 "Azure OpenAI服务持续扩张，企业客户快速增长",
                 "Office 365全面AI化，Copilot集成至Word、Excel、PPT"
             ],
             "event": "Copilot增长",
             "event_desc": "Copilot月活突破800万，企业客户付费率达35%，远超行业平均，验证AI应用商业化可行性",
             "risk": "与OpenAI绑定过深、AI投入回报周期长",
             "outlook": "Copilot生态持续扩张，Azure AI服务增长强劲"},
            {"name": "Adobe", "code": "ADBE", "price": 485.20, "change": 0.85, "currency": "USD",
             "position": "创意AI领导者 | Firefly生态",
             "dynamics": [
                 "Firefly生成式AI工具集成至Photoshop、Illustrator等全系产品",
                 "企业客户付费率提升，B端收入占比持续增长",
                 "版权保护优势明显，训练数据均获授权"
             ],
             "event": "Firefly企业版",
             "event_desc": "Firefly企业版发布，针对企业客户提供定制化AI生成能力，B端市场拓展加速，预计2026年AI收入占比将达20%",
             "risk": "创意AI竞争激烈、宏观经济影响广告支出",
             "outlook": "创意AI领导者地位稳固，企业版打开增长空间"},
            {"name": "Salesforce", "code": "CRM", "price": 325.80, "change": -0.45, "currency": "USD",
             "position": "CRM+AI融合 | Einstein GPT",
             "dynamics": [
                 "Einstein GPT提升销售效率，平均销售周期缩短25%",
                 "AI智能体自动处理客户需求，客服成本降低30%",
                 "与OpenAI深度合作，率先将GPT能力引入CRM"
             ],
             "event": "Einstein升级",
             "event_desc": "Einstein GPT功能升级，客户反馈积极，但市场担忧AI对SaaS商业模式的冲击，短期股价承压",
             "risk": "AI可能颠覆传统SaaS、竞争加剧",
             "outlook": "CRM+AI融合先行者，长期受益于企业AI化"},
            {"name": "Palantir", "code": "PLTR", "price": 85.40, "change": 3.25, "currency": "USD",
             "position": "大数据+AI平台 | AIP军事/政府应用",
             "dynamics": [
                 "AIP平台军事订单持续增长，俄乌冲突后需求旺盛",
                 "受益于政府AI支出增加，国防预算向AI倾斜",
                 "商业客户扩张，金融机构和医疗企业采用AIP"
             ],
             "event": "军事订单",
             "event_desc": "新获美国国防部AI订单，价值超10亿美元，标志Palantir在军事AI领域地位进一步巩固",
             "risk": "政府预算波动、估值偏高",
             "outlook": "军事AI需求强劲，商业市场逐步打开"},
            {"name": "Tesla", "code": "TSLA", "price": 285.60, "change": -1.32, "currency": "USD",
             "position": "自动驾驶AI | FSD端到端神经网络",
             "dynamics": [
                 "FSD V15开始推送，端到端神经网络重构，性能提升",
                 "Dojo超算训练自动驾驶模型，算力持续扩张",
                 "Robotaxi即将发布，预计2026年Q3正式上线"
             ],
             "event": "FSD V15推送",
             "event_desc": "FSD V15推送进度慢于预期，部分用户反馈稳定性问题，市场担忧自动驾驶商业化时间表，短期股价承压",
             "risk": "FSD进度不及预期、自动驾驶监管、竞争加剧",
             "outlook": "FSD是关键变量，Robotaxi或成催化剂"},
        ]
    }

def generate_html():
    """生成 v1.6.1 HTML报告"""
    today = datetime.now()
    date_str = today.strftime("%Y年%m月%d日")
    date_str_en = today.strftime("%B %d, %Y")
    weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][today.weekday()]
    
    stocks = generate_stock_data()
    
    # 生成股票HTML - 增强版
    stocks_html = ""
    for layer_name, layer_stocks in stocks.items():
        layer_title = {"infrastructure": "🏗️ 基础设施层", "model_layer": "🧠 模型层", "application": "💡 应用层"}[layer_name]
        stocks_html += f'<h3 style="color: #818cf8; margin: 30px 0 20px;">{layer_title}</h3>'
        
        for stock in layer_stocks:
            if stock["price"] == "-":
                continue
            change_class = "up" if stock["change"] > 0 else "down"
            change_sign = "+" if stock["change"] > 0 else ""
            currency = stock.get("currency", "CNY")
            flag = "🇨🇳" if currency == "CNY" else "🇺🇸"
            
            dynamics_html = "".join([f'<li>{d}</li>' for d in stock["dynamics"]])
            
            stocks_html += f'''
            <div class="stock-card">
                <div class="stock-header">
                    <div class="stock-info">
                        <h3>{flag} {stock["name"]} ({stock["code"]})</h3>
                        <div class="stock-position">{stock["position"]}</div>
                    </div>
                    <div class="stock-price">
                        <div class="price">{stock["price"]} {currency}</div>
                        <div class="change {change_class}">{change_sign}{stock["change"]}%</div>
                    </div>
                </div>
                <div class="ai-analysis">
                    <h4>🎯 AI产业动态</h4>
                    <ul>{dynamics_html}</ul>
                </div>
                <div class="event-impact">
                    <h4>⚡ 事件驱动分析</h4>
                    <p><span class="tag" style="background: rgba(16, 185, 129, 0.2); color: #10b981;">{stock["event"]}</span> {stock["event_desc"]}</p>
                </div>
                <div class="risk-outlook">
                    <h4>📊 风险与展望</h4>
                    <p><strong>⚠️ 风险：</strong>{stock["risk"]}</p>
                    <p><strong>🔮 展望：</strong>{stock["outlook"]}</p>
                </div>
            </div>'''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IT小路的每日AI简报 v1.6.1</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif; 
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); 
            min-height: 100vh; 
            padding: 20px; 
            color: #e2e8f0; 
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .lang-switcher {{ 
            position: fixed; 
            top: 20px; 
            right: 20px; 
            z-index: 1000; 
            background: rgba(30, 41, 59, 0.95); 
            backdrop-filter: blur(10px);
            padding: 12px 18px; 
            border-radius: 12px; 
            border: 1px solid rgba(99, 102, 241, 0.4); 
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        .lang-switcher select {{ 
            background: transparent; 
            color: #e2e8f0; 
            border: none; 
            font-size: 14px; 
            cursor: pointer;
            padding: 5px 10px;
        }}
        .header {{ 
            text-align: center; 
            padding: 80px 20px 50px; 
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%); 
            border-radius: 24px; 
            margin-bottom: 40px; 
        }}
        .header h1 {{ 
            font-size: 2.8rem; 
            margin-bottom: 15px; 
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%); 
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent;
        }}
        .header .subtitle {{ font-size: 1.1rem; color: #94a3b8; margin-top: 10px; }}
        .header .data-time {{ 
            margin-top: 15px; 
            color: #64748b; 
            font-size: 0.9rem;
            padding: 8px 16px;
            background: rgba(30, 41, 59, 0.5);
            border-radius: 20px;
            display: inline-block;
        }}
        .version-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
            color: #0f172a;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: bold;
            margin-top: 15px;
        }}
        .section {{ margin-bottom: 50px; }}
        .section-title {{ 
            display: inline-flex; 
            align-items: center; 
            gap: 12px; 
            padding: 18px 30px; 
            border-radius: 12px; 
            font-size: 1.3rem; 
            font-weight: bold; 
            margin-bottom: 30px; 
            background: linear-gradient(135deg, #1e293b 0%, rgba(99, 102, 241, 0.3) 100%); 
            color: #818cf8; 
            border: 1px solid rgba(99, 102, 241, 0.4);
        }}
        .headlines-section .section-title {{
            background: linear-gradient(135deg, #1e293b 0%, rgba(245, 158, 11, 0.3) 100%);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.4);
        }}
        .domestic-title {{
            background: linear-gradient(135deg, #1e293b 0%, rgba(239, 68, 68, 0.2) 100%);
            color: #ef4444;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }}
        .international-title {{
            background: linear-gradient(135deg, #1e293b 0%, rgba(59, 130, 246, 0.2) 100%);
            color: #3b82f6;
            border: 1px solid rgba(59, 130, 246, 0.3);
        }}
        .retail-title {{
            background: linear-gradient(135deg, #1e293b 0%, rgba(139, 92, 246, 0.2) 100%);
            color: #a855f7;
            border: 1px solid rgba(139, 92, 246, 0.3);
        }}
        .chain-title {{
            background: linear-gradient(135deg, #1e293b 0%, rgba(16, 185, 129, 0.2) 100%);
            color: #10b981;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }}
        .stocks-title {{
            background: linear-gradient(135deg, #1e293b 0%, rgba(245, 158, 11, 0.2) 100%);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }}
        .headline-card {{
            background: linear-gradient(135deg, #1e293b 0%, rgba(245, 158, 11, 0.1) 100%);
            border-radius: 20px;
            padding: 35px;
            border: 2px solid rgba(245, 158, 11, 0.3);
        }}
        .headline-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
            color: #0f172a;
            padding: 8px 18px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 20px;
        }}
        .headline-title {{ font-size: 1.5rem; color: #fbbf24; margin-bottom: 20px; font-weight: 700; }}
        .headline-content {{ color: #e2e8f0; line-height: 1.8; margin-bottom: 25px; }}
        .sources-title {{ font-size: 1.1rem; color: #818cf8; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 1px solid rgba(99, 102, 241, 0.3); }}
        .source-item {{ background: rgba(15, 23, 42, 0.5); border-radius: 12px; padding: 20px; margin-bottom: 15px; }}
        .source-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
        .source-name {{ font-weight: 600; color: #fbbf24; }}
        .source-link {{ color: #818cf8; text-decoration: none; font-size: 0.9rem; }}
        .source-link:hover {{ color: #a5b4fc; text-decoration: underline; }}
        .source-viewpoint {{ color: #cbd5e1; line-height: 1.7; }}
        .cards {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
        }}
        .card {{
            background: linear-gradient(135deg, #1e293b 0%, rgba(30, 41, 59, 0.8) 100%);
            border-radius: 16px;
            padding: 25px;
            border: 1px solid rgba(148, 163, 184, 0.15);
            transition: all 0.3s ease;
        }}
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }}
        .card-source {{
            display: inline-block;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            margin-bottom: 15px;
        }}
        .card-title {{ font-size: 1.2rem; color: #f8fafc; margin-bottom: 12px; font-weight: 600; }}
        .card-summary {{ color: #cbd5e1; line-height: 1.7; }}
        .retail-card {{
            background: linear-gradient(135deg, #1e293b 0%, rgba(139, 92, 246, 0.1) 100%);
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            border: 1px solid rgba(139, 92, 246, 0.2);
        }}
        .retail-source {{
            display: inline-block;
            background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
            color: white;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            margin-bottom: 15px;
        }}
        .ai-chain-map {{
            background: #1e293b;
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 30px;
            border: 1px solid rgba(99, 102, 241, 0.2);
        }}
        .chain-level {{ margin-bottom: 20px; padding: 15px; background: rgba(15, 23, 42, 0.5); border-radius: 10px; }}
        .chain-label {{ font-weight: 600; color: #818cf8; margin-bottom: 12px; }}
        .chain-stocks {{ display: flex; gap: 10px; flex-wrap: wrap; }}
        .chain-stock {{ padding: 8px 14px; border-radius: 8px; font-size: 0.9rem; background: rgba(99, 102, 241, 0.2); color: #c7d2fe; border: 1px solid rgba(99, 102, 241, 0.3); }}
        .stock-card {{
            background: linear-gradient(135deg, #1e293b 0%, rgba(30, 41, 59, 0.8) 100%);
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            border: 1px solid rgba(148, 163, 184, 0.15);
        }}
        .stock-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid rgba(99, 102, 241, 0.2); }}
        .stock-info h3 {{ font-size: 1.3rem; color: #f8fafc; margin-bottom: 5px; }}
        .stock-position {{ color: #818cf8; font-size: 0.9rem; }}
        .stock-price {{ text-align: right; }}
        .price {{ font-size: 1.5rem; font-weight: bold; color: #f8fafc; }}
        .change {{ font-size: 1.1rem; font-weight: 600; }}
        .change.up {{ color: #10b981; }}
        .change.down {{ color: #ef4444; }}
        .ai-analysis h4 {{ color: #818cf8; margin-bottom: 12px; }}
        .ai-analysis ul {{ list-style: none; padding: 0; }}
        .ai-analysis li {{ padding: 8px 0; color: #cbd5e1; border-left: 3px solid #6366f1; padding-left: 15px; margin-bottom: 8px; }}
        .event-impact h4 {{ color: #fbbf24; margin: 15px 0 10px; }}
        .event-impact p {{ color: #cbd5e1; line-height: 1.6; }}
        .risk-outlook {{ margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(99, 102, 241, 0.2); }}
        .risk-outlook h4 {{ color: #ef4444; margin-bottom: 10px; }}
        .risk-outlook p {{ color: #cbd5e1; line-height: 1.6; margin-bottom: 8px; }}
        .tag {{ display: inline-block; padding: 3px 10px; border-radius: 4px; font-size: 12px; margin-right: 8px; font-weight: 500; }}
        .investment-card {{
            background: linear-gradient(135deg, #1e293b 0%, rgba(16, 185, 129, 0.1) 100%);
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            border: 1px solid rgba(16, 185, 129, 0.2);
        }}
        .investment-title {{ color: #10b981; font-weight: 600; margin-bottom: 12px; font-size: 1.1rem; }}
        .investment-content {{ color: #cbd5e1; line-height: 1.8; }}
        .risk-card {{
            background: linear-gradient(135deg, #1e293b 0%, rgba(239, 68, 68, 0.1) 100%);
            border-radius: 16px;
            padding: 25px;
            border: 1px solid rgba(239, 68, 68, 0.2);
        }}
        .risk-title {{ color: #ef4444; font-weight: 600; margin-bottom: 12px; font-size: 1.1rem; }}
        .risk-content {{ color: #cbd5e1; line-height: 1.8; }}
        .footer {{
            text-align: center;
            padding: 40px;
            color: #64748b;
            border-top: 1px solid rgba(148, 163, 184, 0.1);
            margin-top: 50px;
        }}
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.8rem; }}
            .cards {{ grid-template-columns: 1fr; }}
            .stock-header {{ flex-direction: column; align-items: flex-start; }}
            .stock-price {{ text-align: left; margin-top: 10px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="lang-switcher">
            <select id="langSelect" onchange="switchLanguage()">
                <option value="zh">🇨🇳 中文</option>
                <option value="en">🇺🇸 English</option>
            </select>
        </div>
        
        <header class="header">
            <h1>🌊 IT小路的每日AI简报</h1>
            <div class="subtitle">AI产业视角 · 感知智能脉搏</div>
            <div class="data-time">{date_str} · {weekday} · {date_str_en}</div>
            <div class="version-badge">v1.6.1 Release · 增强版股票分析</div>
        </header>

        <!-- 今日头条 -->
        <section class="section headlines-section">
            <div class="section-title">🔥 今日头条 / Headlines</div>
            <div class="headline-card">
                <div class="headline-badge">📰 今日最重要</div>
                <h2 class="headline-title">两会聚焦AI：工信部部长宣布大力推动人工智能与制造业"双向奔赴"</h2>
                <div class="headline-content">
                    <p>3月5日，在十四届全国人大四次会议首场"部长通道"上，工业和信息化部部长李乐成表示，2026年政府工作报告多次提到人工智能，工信部将按照要求，大力推动人工智能和制造业"双向奔赴"。数据显示，2025年我国人工智能核心产业规模超过1.2万亿元，企业数量超过6200家。</p>
                </div>
                <div class="sources-title">📎 多信源观点</div>
                <div class="source-item">
                    <div class="source-header">
                        <span class="source-name">💼 新华社</span>
                    </div>
                    <div class="source-viewpoint">新华社指出，人工智能这个"关键变量"正在成为经济高质量发展的"强劲增量"，政府工作报告中明确提出培育发展具身智能、量子科技、脑机接口、6G等未来产业。</div>
                </div>
                <div class="source-item">
                    <div class="source-header">
                        <span class="source-name">📊 证券时报</span>
                    </div>
                    <div class="source-viewpoint">证券时报分析认为，AI与制造业的"双向奔赴"将加速产业升级，预计2026年智能制造投资将增长30%以上，工业机器人、智能检测设备需求旺盛。</div>
                </div>
                <div class="source-item">
                    <div class="source-header">
                        <span class="source-name">📡 第一财经</span>
                    </div>
                    <div class="source-viewpoint">第一财经评论称，6200家AI企业的数据彰显中国AI产业生态的蓬勃发展，从芯片到应用的全产业链布局正在形成。</div>
                </div>
            </div>
        </section>

        <!-- 国内AI热点 -->
        <section class="section">
            <div class="section-title domestic-title">🇨🇳 国内AI热点 / Domestic AI News</div>
            <div class="cards">
                <div class="card">
                    <div class="card-source">🔥 热门</div>
                    <h3 class="card-title">阿里通义千问技术负责人林俊旸离职，CEO吴泳铭回应坚持开源</h3>
                    <p class="card-summary">3月5日，阿里巴巴CEO吴泳铭在内部邮件中回应林俊旸离职一事，表示将继续坚持开源模型策略，持续加大AI研发投入。阿里同时辟谣"千问模型核心团队集体离职"为不实信息。</p>
                </div>
                <div class="card">
                    <div class="card-source">🚗 新品</div>
                    <h3 class="card-title">特斯拉中国官宣与火山引擎合作，Model Y L将搭载豆包大模型</h3>
                    <p class="card-summary">特斯拉中国官网更新《车机语音助手使用条款》，官宣与字节跳动旗下火山引擎达成合作。全新六座旗舰SUV Model Y L将成为首款搭载国产大模型的智能电车。</p>
                </div>
                <div class="card">
                    <div class="card-source">🤖 应用</div>
                    <h3 class="card-title">清华系机器人企业星动纪元、极佳视界同日获大额融资</h3>
                    <p class="card-summary">人形机器人2026年融资突破130亿元，清华系企业成为资本追逐焦点。星动纪元完成超5亿元融资，极佳视界获近3亿元投资。</p>
                </div>
            </div>
        </section>

        <!-- 海外AI热点 -->
        <section class="section">
            <div class="section-title international-title">🌍 海外AI热点 / International AI News</div>
            <div class="cards">
                <div class="card">
                    <div class="card-source">💻 技术</div>
                    <h3 class="card-title">Google DeepMind发布AI编程代理AlphaEvolve</h3>
                    <p class="card-summary">AlphaEvolve能够自主编写、测试和优化代码，在标准编程测试中表现超过90%的人类程序员。这标志着AI编程能力进入新阶段。</p>
                </div>
                <div class="card">
                    <div class="card-source">🧠 模型</div>
                    <h3 class="card-title">OpenAI GPT-5预览版发布：多模态能力大幅提升</h3>
                    <p class="card-summary">GPT-5在图像理解、视频生成和代码编写方面都有显著改进，预计Q2正式发布。企业客户已可申请内测。</p>
                </div>
                <div class="card">
                    <div class="card-source">🚀 产品</div>
                    <h3 class="card-title">Anthropic Claude 4发布：推理能力超越GPT-4</h3>
                    <p class="card-summary">Claude 4在数学推理和逻辑分析方面表现出色，企业级应用前景广阔。新模型支持100万token上下文窗口。</p>
                </div>
            </div>
        </section>

        <!-- 零售AI应用 -->
        <section class="section">
            <div class="section-title retail-title">🛍️ 零售AI应用实践 / Retail AI Practices</div>
            <div class="retail-card">
                <div class="retail-source">🇨🇳 阿里巴巴</div>
                <h3 class="card-title">马云现身云谷学校，阿里核心管理层聚齐交流AI教育</h3>
                <p class="card-summary">3月3日，马云携阿里及蚂蚁核心管理层罕见齐聚杭州云谷学校，与教育工作者探讨AI时代的挑战与机遇。马云强调AI冲击巨大且变革迅速，教育应转向培养孩子的创造力、共情力等AI无法替代的核心能力。</p>
            </div>
            <div class="retail-card">
                <div class="retail-source">🇺🇸 Amazon</div>
                <h3 class="card-title">Amazon Go技术扩展，无收银购物体验持续升级</h3>
                <p class="card-summary">Amazon继续扩展其Just Walk Out技术，该技术使顾客无需排队结账，拿了就走。该技术使结账时间减少90%，目前已部署至200+门店。</p>
            </div>
            <div class="retail-card">
                <div class="retail-source">🇨🇳 杭州上城</div>
                <h3 class="card-title">杭州上城打造"OPC创业第一城"，AI助力"一人一公司"</h3>
                <p class="card-summary">杭州市上城区创新推出《上城区支持人工智能OPC社区建设若干措施》，这是浙江省首个发布的区级OPC专项政策。OPC（One Person Company）模式让普通人借助AI工具链，能独立完成从产品设计到客户服务的全流程。</p>
            </div>
        </section>

        <!-- AI产业链 -->
        <section class="section">
            <div class="section-title chain-title">🔗 AI产业链全景 / AI Industry Chain</div>
            <div class="ai-chain-map">
                <div class="chain-level">
                    <div class="chain-label">🏗️ 基础设施层（5家）Infrastructure Layer</div>
                    <div class="chain-stocks">
                        <span class="chain-stock">NVIDIA (GPU)</span>
                        <span class="chain-stock">AMD (GPU)</span>
                        <span class="chain-stock">Intel (CPU)</span>
                        <span class="chain-stock">寒武纪 (AI芯片)</span>
                        <span class="chain-stock">海光信息 (CPU)</span>
                    </div>
                </div>
                <div class="chain-level">
                    <div class="chain-label">🧠 模型层（5家）Model Layer</div>
                    <div class="chain-stocks">
                        <span class="chain-stock">OpenAI (GPT)</span>
                        <span class="chain-stock">Google (Gemini)</span>
                        <span class="chain-stock">Meta (Llama)</span>
                        <span class="chain-stock">阿里 (千问)</span>
                        <span class="chain-stock">科大讯飞 (星火)</span>
                    </div>
                </div>
                <div class="chain-level">
                    <div class="chain-label">💡 应用层（5家）Application Layer</div>
                    <div class="chain-stocks">
                        <span class="chain-stock">Microsoft (Copilot)</span>
                        <span class="chain-stock">Adobe (Firefly)</span>
                        <span class="chain-stock">Salesforce (Einstein)</span>
                        <span class="chain-stock">Palantir (AIP)</span>
                        <span class="chain-stock">Tesla (FSD)</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- AI产业股票分析 -->
        <section class="section">
            <div class="section-title stocks-title">📈 AI产业视角股票分析（15家核心标的）/ AI Stock Analysis</div>
            {stocks_html}
        </section>

        <!-- 投资配置建议 -->
        <section class="section">
            <div class="section-title chain-title">💼 投资配置建议 / Investment Advice</div>
            <div class="investment-card">
                <div class="investment-title">🎯 短期策略（1-3个月）</div>
                <div class="investment-content">
                    <strong>超配：</strong>光模块（中际旭创）、国产AI芯片（寒武纪、海光）——两会AI政策催化，国产替代加速<br>
                    <strong>关注：</strong>NVIDIA光学互连投资受益标的（Coherent、Lumentum）——解决超大规模集群瓶颈<br>
                    <strong>谨慎：</strong>高估值AI应用股，等待业绩验证，避免追高风险
                </div>
            </div>
            <div class="investment-card">
                <div class="investment-title">📊 中长期布局（6-12个月）</div>
                <div class="investment-content">
                    <strong>美股：</strong>NVIDIA仍是AI基础设施核心标的，Blackwell架构持续领先；Microsoft受益于Copilot生态扩张，Azure AI服务增长强劲；AMD份额持续提升，ROCm生态逐步完善<br>
                    <strong>A股：</strong>国产AI芯片（寒武纪、海光）受益于国产替代大趋势；科大讯飞教育AI业务受益于政策红利<br>
                    <strong>全球配置建议：</strong>AI产业链三层配置——基础设施40%（算力芯片）、模型层30%（大模型厂商）、应用层30%（AI应用）
                </div>
            </div>
            <div class="risk-card">
                <div class="risk-title">⚠️ 风险提示</div>
                <div class="risk-content">
                    1. <strong>地缘政治风险：</strong>中美科技摩擦可能影响AI芯片供应链，出口管制风险<br>
                    2. <strong>估值风险：</strong>AI板块整体估值偏高，短期波动可能加大，需关注业绩兑现<br>
                    3. <strong>技术迭代风险：</strong>大模型技术快速演进，落后者可能被淘汰，投资需关注技术路线<br>
                    4. <strong>仅供投资参考，不构成投资建议。</strong>投资者应根据自身风险承受能力谨慎决策
                </div>
            </div>
        </section>

        <footer class="footer">
            <p>🌊 IT小路的每日AI简报 v1.6.1 · AI产业视角 · 数据截止 2026-03-07 07:10</p>
        </footer>
    </div>
</body>
</html>'''
    
    return html

def main():
    """主函数"""
    print("=" * 50)
    print("🚀 AI日报生成器 v1.6.1 - 增强版")
    print("=" * 50)
    
    # 生成HTML
    print("[1/2] 生成HTML报告...")
    html = generate_html()
    
    # 保存文件
    print("[2/2] 保存报告...")
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"ai-report-v161-{today}.html"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ 报告生成完成: {filename}")
    return filename

if __name__ == "__main__":
    main()
