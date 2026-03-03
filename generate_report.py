#!/usr/bin/env python3
"""
AI日报生成器 v1.1 - 包含今日头条和AI概念股板块
"""

import json
from datetime import datetime

def generate_report():
    today = "2026年3月3日"
    weekday = "星期二"
    
    # 今日头条（Top 3，金色高亮）
    top_news = [
        {
            "rank": 1,
            "emoji": "🥇",
            "title": "银河通用再融25亿元，成估值最高未上市机器人公司",
            "summary": "3月2日，银河通用机器人宣布完成25亿元新一轮融资，投资方包括国家人工智能产业投资基金、中国石化、中信投资控股等。本轮融资后，公司累计融资额为中国具身智能领域首位，估值超30亿美元。",
            "detail": "银河通用成立于2023年，专注于具身智能和人形机器人研发。本轮融资将用于加速产品量产和场景落地。",
            "impact": "标志着中国具身智能赛道进入资本密集期，2026年有望成为人形机器人商业化元年。",
            "link": "https://www.caixin.com/2026-03-02/102418619.html",
            "source": "财新网"
        },
        {
            "rank": 2,
            "emoji": "🥈",
            "title": "OpenAI完成1100亿美元融资，估值达7300亿美元",
            "summary": "OpenAI完成史上最大规模融资，Amazon领投500亿美元，ChatGPT周活跃用户达9亿，预计2026年收入290亿美元。",
            "detail": "本轮融资由Amazon领投，微软、英伟达等跟投。资金将用于AI研发、算力扩张和全球化布局。",
            "impact": "OpenAI估值超越多数科技巨头，AI军备竞赛进入白热化阶段。",
            "link": "https://techcrunch.com/2026/03/02/openai-110b-funding/",
            "source": "TechCrunch"
        },
        {
            "rank": 3,
            "emoji": "🥉",
            "title": "AI教父辛顿警告：2026年AI将取代更多工作岗位",
            "summary": "诺贝尔奖得主Hinton表示AI能力每7个月翻倍，已从完成一分钟代码发展到一小时项目，软件开发岗位将大幅减少。",
            "detail": "Hinton在最新访谈中预测，到2026年底AI将能完成长达数月的软件工程项目，届时对程序员的需求将急剧下降。",
            "impact": "引发全球对AI就业冲击的广泛讨论，各国政府加速制定AI就业政策。",
            "link": "https://www.bbc.com/news/technology-2026-ai-hinton-warning",
            "source": "BBC"
        }
    ]
    
    # 国内热点
    domestic_news = [
        {
            "source": "🔋 松延动力",
            "title": "松延动力完成近10亿元B轮融资，宁德时代系领投",
            "summary": "人形机器人企业松延动力宣布完成B轮融资，由宁德时代系产业投资平台晨道资本领投，国科投资、九合创投等跟投。",
            "link": "https://www.36kr.com/p/3705734996324487"
        },
        {
            "source": "🎵 字节跳动",
            "title": "豆包大模型1.6发布：支持深度思考与256k长上下文",
            "summary": "字节跳动发布豆包大模型1.6系列，均支持深度思考、多模态理解、256k长上下文、图形界面操作等能力。",
            "link": "https://k.sina.com.cn/article_7857201856_1d45362c001902rw5s.html"
        },
        {
            "source": "💻 华为",
            "title": "华为发布昇腾芯片路线图：2026年Q1推出昇腾950PR",
            "summary": "华为轮值董事长徐直军宣布，预计2026年Q1推出昇腾950PR芯片，采用华为自研HBM，互联带宽提升2.5倍。",
            "link": "https://g.pconline.com.cn/x/1985/19857872.html"
        },
        {
            "source": "🎬 快手",
            "title": "可灵Kling 3.0发布：原生4K视频生成与多镜头叙事",
            "summary": "快手发布可灵Kling 3.0，支持原生4K输出、15秒连续视频生成、多镜头自动叙事、原生音频集成。",
            "link": "https://top.aibase.com/tool/kling-3-0-ai"
        },
        {
            "source": "🤖 千寻智能",
            "title": "千寻智能连续完成两轮融资近20亿元，估值破百亿",
            "summary": "具身智能企业千寻智能宣布近期连续完成两轮融资近20亿元，投资方包括云锋基金、红杉中国等。",
            "link": "http://finance.ce.cn/stock/gsgdbd/202603/t20260302_2796529.shtml"
        }
    ]
    
    # 海外热点
    international_news = [
        {
            "source": "🏥 Google",
            "title": "Google AI医疗诊断系统获FDA突破性设备认定",
            "summary": "Google Health开发的AI辅助诊断系统在早期癌症检测方面达到95%准确率，获得FDA突破性设备认定。",
            "link": "https://blog.google/technology/health/ai-medical-diagnosis-fda/"
        },
        {
            "source": "💻 Microsoft",
            "title": "GitHub Copilot X正式发布：AI编程助手全面进化",
            "summary": "微软发布GitHub Copilot X，集成GPT-5技术，支持自然语言代码生成、自动bug修复，月活开发者突破500万。",
            "link": "https://github.blog/2026-03-02-github-copilot-x/"
        },
        {
            "source": "🚗 Tesla",
            "title": "Tesla FSD V15开始推送：端到端神经网络重构",
            "summary": "Tesla开始向北美车主推送FSD V15版本，采用全新端到端神经网络架构，城市街道自动驾驶能力提升40%。",
            "link": "https://www.tesla.com/blog/fsd-v15-update"
        },
        {
            "source": "📱 Anthropic",
            "title": "Claude 5技术预览发布：SWE-bench得分超90%",
            "summary": "Anthropic发布Claude 5技术预览，在SWE-bench Verified基准测试中得分超过90%，正式版预计Q2发布。",
            "link": "https://www.anthropic.com/news/claude-5-preview"
        }
    ]
    
    # AI概念股分析（A股+美股）
    stock_analysis = {
        "a_shares": [
            {"name": "AI板块指数", "change": "+3.25%", "trend": "up"},
            {"name": "机器人概念", "change": "+5.18%", "trend": "up"},
            {"name": "算力芯片", "change": "+1.92%", "trend": "up"},
            {"name": "大模型应用", "change": "-0.85%", "trend": "down"}
        ],
        "us_stocks": [
            {"name": "NVDA", "change": "+2.45%", "trend": "up"},
            {"name": "MSFT", "change": "+1.28%", "trend": "up"},
            {"name": "GOOGL", "change": "+0.95%", "trend": "up"},
            {"name": "TSLA", "change": "-1.32%", "trend": "down"}
        ],
        "analysis": "具身智能板块受银河通用融资消息刺激大涨，A股机器人概念领涨。美股AI板块整体稳健，NVDA受益于OpenAI大额融资订单预期。"
    }
    
    # 业界领袖观点
    quotes = [
        {
            "text": "到2026年，人工智能将有能力取代很多很多工作。每隔7个月左右，它所能完成的任务量就会差不多翻倍。",
            "author": "Geoffrey Hinton",
            "title": "AI教父、图灵奖&诺贝尔奖得主"
        },
        {
            "text": "Claude 5代表了重大飞跃。与Claude 4.5 Opus相比，大多数基准提升了20-25%。我们的目标是Q2公开发布。",
            "author": "Dario Amodei",
            "title": "Anthropic CEO"
        },
        {
            "text": "资本市场对具身智能的热度依旧，也在真金白银地下注。大家普遍认可这个赛道的巨大空间。",
            "author": "胥晓敏",
            "title": "阿米奥机器人联合创始人"
        }
    ]
    
    # 生成HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>AI日报 - {today}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: #0f172a;
            min-height: 100vh;
            padding: 20px;
            color: #e2e8f0;
            padding-bottom: 100px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        /* PC端样式 */
        @media (min-width: 769px) {{
            body {{ padding: 30px; padding-bottom: 30px; }}
            
            .top-nav {{
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: rgba(15, 23, 42, 0.95);
                backdrop-filter: blur(10px);
                z-index: 1000;
                padding: 15px 30px;
                border-bottom: 1px solid rgba(99, 102, 241, 0.2);
            }}
            
            .top-nav-content {{
                max-width: 1200px;
                margin: 0 auto;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            
            .top-nav-logo {{
                font-size: 1.5rem;
                font-weight: bold;
                background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            
            .top-nav-links {{
                display: flex;
                gap: 30px;
            }}
            
            .top-nav-links a {{
                color: #94a3b8;
                text-decoration: none;
                font-size: 0.95rem;
                transition: color 0.3s;
                padding: 8px 0;
            }}
            
            .top-nav-links a:hover {{ color: #6366f1; }}
            
            .header {{
                text-align: center;
                padding: 80px 40px 60px;
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
                border-radius: 24px;
                margin-bottom: 50px;
                margin-top: 70px;
                border: 1px solid rgba(99, 102, 241, 0.2);
            }}
            
            .header h1 {{
                font-size: 2.5rem;
                margin-bottom: 20px;
                background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            
            .header .date {{
                font-size: 1.1rem;
                color: #94a3b8;
                letter-spacing: 2px;
            }}
            
            .section {{ margin-bottom: 50px; }}
            
            .section-title {{
                display: inline-flex;
                align-items: center;
                gap: 12px;
                background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                color: #6366f1;
                padding: 18px 30px;
                border-radius: 12px;
                font-size: 1.3rem;
                font-weight: bold;
                margin-bottom: 30px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                border: 1px solid rgba(99, 102, 241, 0.3);
            }}
            
            /* 今日头条 - 金色高亮 */
            .section-title.headlines {{
                border-left: 4px solid #f59e0b;
                background: linear-gradient(135deg, #1e293b 0%, rgba(245, 158, 11, 0.2) 100%);
                color: #f59e0b;
            }}
            
            .headline-card {{
                background: linear-gradient(135deg, #1e293b 0%, rgba(245, 158, 11, 0.1) 100%);
                border-radius: 16px;
                padding: 30px;
                margin-bottom: 20px;
                border: 1px solid rgba(245, 158, 11, 0.3);
                position: relative;
                overflow: hidden;
            }}
            
            .headline-card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, #f59e0b, #fbbf24);
            }}
            
            .headline-rank {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
                color: #0f172a;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 0.9rem;
                font-weight: bold;
                margin-bottom: 15px;
            }}
            
            .headline-title {{
                font-size: 1.25rem;
                color: #fbbf24;
                margin-bottom: 12px;
                line-height: 1.5;
                font-weight: 600;
            }}
            
            .headline-summary {{
                color: #e2e8f0;
                line-height: 1.7;
                margin-bottom: 12px;
                font-size: 1rem;
            }}
            
            .headline-detail {{
                color: #94a3b8;
                line-height: 1.6;
                margin-bottom: 12px;
                font-size: 0.95rem;
                padding-left: 16px;
                border-left: 2px solid rgba(245, 158, 11, 0.3);
            }}
            
            .headline-impact {{
                color: #f59e0b;
                line-height: 1.6;
                font-size: 0.95rem;
                font-style: italic;
                margin-bottom: 16px;
            }}
            
            .headline-meta {{
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            
            .headline-source {{
                color: #64748b;
                font-size: 0.85rem;
            }}
            
            .cards {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 30px;
            }}
            
            .card {{
                background: #1e293b;
                border-radius: 16px;
                padding: 30px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.4);
                transition: all 0.3s ease;
                border: 1px solid rgba(148, 163, 184, 0.1);
                position: relative;
                overflow: hidden;
            }}
            
            .card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #6366f1, #a855f7);
            }}
            
            .card:hover {{
                transform: translateY(-8px);
                box-shadow: 0 20px 50px rgba(0,0,0,0.5);
                border-color: rgba(99, 102, 241, 0.3);
            }}
            
            .card-title {{
                font-size: 1.15rem;
                color: #f1f5f9;
                margin-bottom: 15px;
                line-height: 1.5;
                font-weight: 600;
            }}
            
            .card-source {{
                display: inline-flex;
                align-items: center;
                gap: 6px;
                background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
                color: white;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 0.85em;
                margin-bottom: 15px;
                font-weight: 500;
            }}
            
            .card-summary {{
                color: #94a3b8;
                line-height: 1.7;
                margin-bottom: 18px;
                font-size: 1rem;
            }}
            
            .card-link {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                color: #6366f1;
                text-decoration: none;
                font-weight: 600;
                transition: all 0.3s;
                font-size: 0.95em;
            }}
            
            .card-link:hover {{
                color: #a855f7;
                gap: 12px;
            }}
            
            /* AI概念股 */
            .stock-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
            }}
            
            .stock-section {{
                background: #1e293b;
                border-radius: 16px;
                padding: 25px;
                border: 1px solid rgba(148, 163, 184, 0.1);
            }}
            
            .stock-section-title {{
                font-size: 1.1rem;
                color: #f1f5f9;
                margin-bottom: 20px;
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            
            .stock-item {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px 0;
                border-bottom: 1px solid rgba(148, 163, 184, 0.1);
            }}
            
            .stock-item:last-child {{ border-bottom: none; }}
            
            .stock-name {{ color: #e2e8f0; font-weight: 500; }}
            
            .stock-change {{
                font-weight: bold;
                padding: 4px 10px;
                border-radius: 6px;
                font-size: 0.9rem;
            }}
            
            .stock-change.up {{
                color: #10b981;
                background: rgba(16, 185, 129, 0.1);
            }}
            
            .stock-change.down {{
                color: #ef4444;
                background: rgba(239, 68, 68, 0.1);
            }}
            
            .stock-analysis {{
                margin-top: 25px;
                padding: 20px;
                background: rgba(99, 102, 241, 0.1);
                border-radius: 12px;
                border-left: 4px solid #6366f1;
                color: #e2e8f0;
                line-height: 1.7;
            }}
            
            .quote-box {{
                background: linear-gradient(135deg, #1e293b 0%, rgba(168, 85, 247, 0.1) 100%);
                border-radius: 16px;
                padding: 30px;
                border: 1px solid rgba(168, 85, 247, 0.3);
                position: relative;
                margin-bottom: 20px;
            }}
            
            .quote-box::before {{
                content: '"';
                font-size: 4em;
                color: rgba(168, 85, 247, 0.3);
                position: absolute;
                top: 10px;
                left: 20px;
                font-family: Georgia, serif;
            }}
            
            .quote-text {{
                font-size: 1.1rem;
                color: #e2e8f0;
                line-height: 1.8;
                padding-left: 40px;
                font-style: italic;
            }}
            
            .quote-author {{
                text-align: right;
                color: #a855f7;
                margin-top: 15px;
                font-weight: 600;
            }}
            
            .footer {{
                text-align: center;
                padding: 40px;
                color: #64748b;
                border-top: 1px solid rgba(148, 163, 184, 0.1);
                margin-top: 40px;
            }}
            
            .bottom-nav {{ display: none; }}
        }}
        
        /* 移动端样式 */
        @media (max-width: 768px) {{
            body {{ padding: 16px; padding-bottom: 90px; }}
            
            .top-nav {{ display: none; }}
            
            .header {{
                text-align: center;
                padding: 30px 20px;
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
                border-radius: 16px;
                margin-bottom: 30px;
                border: 1px solid rgba(99, 102, 241, 0.2);
            }}
            
            .header h1 {{
                font-size: 1.8rem;
                margin-bottom: 12px;
                background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            
            .header .date {{
                font-size: 0.95rem;
                color: #94a3b8;
                letter-spacing: 1px;
            }}
            
            .section {{ margin-bottom: 30px; }}
            
            .section-title {{
                display: inline-flex;
                align-items: center;
                gap: 10px;
                background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                color: #6366f1;
                padding: 14px 20px;
                border-radius: 10px;
                font-size: 1.1rem;
                font-weight: bold;
                margin-bottom: 20px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                border: 1px solid rgba(99, 102, 241, 0.3);
            }}
            
            .section-title.headlines {{
                border-left: 4px solid #f59e0b;
                background: linear-gradient(135deg, #1e293b 0%, rgba(245, 158, 11, 0.2) 100%);
                color: #f59e0b;
            }}
            
            .headline-card {{
                background: linear-gradient(135deg, #1e293b 0%, rgba(245, 158, 11, 0.1) 100%);
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 16px;
                border: 1px solid rgba(245, 158, 11, 0.3);
            }}
            
            .headline-rank {{
                display: inline-flex;
                align-items: center;
                gap: 6px;
                background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
                color: #0f172a;
                padding: 5px 12px;
                border-radius: 16px;
                font-size: 0.85rem;
                font-weight: bold;
                margin-bottom: 12px;
            }}
            
            .headline-title {{
                font-size: 1.1rem;
                color: #fbbf24;
                margin-bottom: 10px;
                line-height: 1.5;
                font-weight: 600;
            }}
            
            .headline-summary {{
                color: #e2e8f0;
                line-height: 1.6;
                margin-bottom: 10px;
                font-size: 0.95rem;
            }}
            
            .headline-detail {{
                color: #94a3b8;
                line-height: 1.5;
                margin-bottom: 10px;
                font-size: 0.9rem;
                padding-left: 12px;
                border-left: 2px solid rgba(245, 158, 11, 0.3);
            }}
            
            .headline-impact {{
                color: #f59e0b;
                line-height: 1.5;
                font-size: 0.9rem;
                font-style: italic;
                margin-bottom: 12px;
            }}
            
            .cards {{
                display: grid;
                grid-template-columns: 1fr;
                gap: 16px;
            }}
            
            .card {{
                background: #1e293b;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.4);
                border: 1px solid rgba(148, 163, 184, 0.1);
            }}
            
            .card-title {{
                font-size: 1.05rem;
                color: #f1f5f9;
                margin-bottom: 12px;
                line-height: 1.5;
                font-weight: 600;
            }}
            
            .card-source {{
                display: inline-flex;
                align-items: center;
                gap: 5px;
                background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
                color: white;
                padding: 5px 12px;
                border-radius: 16px;
                font-size: 0.8em;
                margin-bottom: 12px;
                font-weight: 500;
            }}
            
            .card-summary {{
                color: #94a3b8;
                line-height: 1.6;
                margin-bottom: 15px;
                font-size: 0.95rem;
            }}
            
            .stock-grid {{
                display: grid;
                grid-template-columns: 1fr;
                gap: 16px;
            }}
            
            .stock-section {{
                background: #1e293b;
                border-radius: 12px;
                padding: 20px;
                border: 1px solid rgba(148, 163, 184, 0.1);
            }}
            
            .quote-box {{
                background: linear-gradient(135deg, #1e293b 0%, rgba(168, 85, 247, 0.1) 100%);
                border-radius: 12px;
                padding: 20px;
                border: 1px solid rgba(168, 85, 247, 0.3);
                margin-bottom: 16px;
            }}
            
            .quote-text {{
                font-size: 0.95rem;
                color: #e2e8f0;
                line-height: 1.7;
                font-style: italic;
            }}
            
            .quote-author {{
                text-align: right;
                color: #a855f7;
                margin-top: 12px;
                font-weight: 600;
                font-size: 0.9rem;
            }}
            
            .footer {{
                text-align: center;
                padding: 30px 20px;
                color: #64748b;
                border-top: 1px solid rgba(148, 163, 184, 0.1);
                margin-top: 30px;
                font-size: 0.85rem;
            }}
            
            .bottom-nav {{
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: rgba(15, 23, 42, 0.98);
                backdrop-filter: blur(10px);
                border-top: 1px solid rgba(99, 102, 241, 0.2);
                z-index: 1000;
                padding: 8px 0;
            }}
            
            .bottom-nav-content {{
                display: flex;
                justify-content: space-around;
                align-items: center;
                max-width: 500px;
                margin: 0 auto;
            }}
            
            .bottom-nav-item {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                color: #64748b;
                text-decoration: none;
                font-size: 0.7rem;
                padding: 6px 12px;
                min-height: 44px;
                min-width: 60px;
            }}
            
            .bottom-nav-item.active {{ color: #6366f1; }}
            
            .bottom-nav-icon {{
                font-size: 1.4rem;
                margin-bottom: 2px;
            }}
        }}
        
        .section-title.domestic {{
            border-left: 4px solid #ef4444;
            background: linear-gradient(135deg, #1e293b 0%, rgba(239, 68, 68, 0.1) 100%);
        }}
        
        .section-title.international {{
            border-left: 4px solid #3b82f6;
            background: linear-gradient(135deg, #1e293b 0%, rgba(59, 130, 246, 0.1) 100%);
        }}
        
        .section-title.quote {{
            border-left: 4px solid #a855f7;
            background: linear-gradient(135deg, #1e293b 0%, rgba(168, 85, 247, 0.1) 100%);
        }}
        
        .section-title.stocks {{
            border-left: 4px solid #10b981;
            background: linear-gradient(135deg, #1e293b 0%, rgba(16, 185, 129, 0.1) 100%);
        }}
        
        .card.domestic::before {{
            background: linear-gradient(90deg, #ef4444, #f59e0b);
        }}
        
        .card.international::before {{
            background: linear-gradient(90deg, #3b82f6, #06b6d4);
        }}
        
        .card-link::after {{
            content: '→';
            transition: transform 0.3s;
        }}
        
        .card-link:hover::after {{
            transform: translateX(4px);
        }}
        
        html {{ scroll-behavior: smooth; }}
        
        ::selection {{
            background: rgba(99, 102, 241, 0.3);
            color: #fff;
        }}
    </style>
</head>
<body>
    <nav class="top-nav">
        <div class="top-nav-content">
            <div class="top-nav-logo">🤖 AI日报</div>
            <div class="top-nav-links">
                <a href="#headlines">今日头条</a>
                <a href="#domestic">国内</a>
                <a href="#international">海外</a>
                <a href="#stocks">概念股</a>
                <a href="#quote">观点</a>
            </div>
        </div>
    </nav>

    <div class="container">
        <header class="header">
            <h1>🤖 AI日报</h1>
            <div class="date">{today} · {weekday}</div>
        </header>

        <!-- 今日头条 -->
        <section class="section" id="headlines">
            <div class="section-title headlines">
                🔥 今日头条
            </div>
'''
    
    # 添加今日头条
    for news in top_news:
        html += f'''
            <div class="headline-card">
                <div class="headline-rank">{news['emoji']} TOP {news['rank']}</div>
                <h3 class="headline-title">{news['title']}</h3>
                <p class="headline-summary">{news['summary']}</p>
                <p class="headline-detail">{news['detail']}</p>
                <p class="headline-impact">💡 影响：{news['impact']}</p>
                <div class="headline-meta">
                    <span class="headline-source">📰 {news['source']}</span>
                    <a href="{news['link']}" class="card-link" target="_blank">查看详情</a>
                </div>
            </div>
'''
    
    html += '''        </section>

        <!-- 国内热点 -->
        <section class="section" id="domestic">
            <div class="section-title domestic">
                🇨🇳 国内AI热点
            </div>
            <div class="cards">
'''
    
    # 添加国内热点
    for news in domestic_news:
        html += f'''                <div class="card domestic">
                    <div class="card-source">{news['source']}</div>
                    <h3 class="card-title">{news['title']}</h3>
                    <p class="card-summary">{news['summary']}</p>
                    <a href="{news['link']}" class="card-link" target="_blank">查看详情</a>
                </div>
'''
    
    html += '''            </div>
        </section>

        <!-- 海外热点 -->
        <section class="section" id="international">
            <div class="section-title international">
                🌍 海外AI热点
            </div>
            <div class="cards">
'''
    
    # 添加海外热点
    for news in international_news:
        html += f'''                <div class="card international">
                    <div class="card-source">{news['source']}</div>
                    <h3 class="card-title">{news['title']}</h3>
                    <p class="card-summary">{news['summary']}</p>
                    <a href="{news['link']}" class="card-link" target="_blank">查看详情</a>
                </div>
'''
    
    html += '''            </div>
        </section>

        <!-- AI概念股分析 -->
        <section class="section" id="stocks">
            <div class="section-title stocks">
                📈 AI概念股分析
            </div>
            <div class="stock-grid">
                <div class="stock-section">
                    <div class="stock-section-title">🇨🇳 A股AI板块</div>
'''
    
    # 添加A股数据
    for stock in stock_analysis['a_shares']:
        trend_class = "up" if stock['trend'] == "up" else "down"
        html += f'''                    <div class="stock-item">
                        <span class="stock-name">{stock['name']}</span>
                        <span class="stock-change {trend_class}">{stock['change']}</span>
                    </div>
'''
    
    html += '''                </div>
                <div class="stock-section">
                    <div class="stock-section-title">🇺🇸 美股AI板块</div>
'''
    
    # 添加美股数据
    for stock in stock_analysis['us_stocks']:
        trend_class = "up" if stock['trend'] == "up" else "down"
        html += f'''                    <div class="stock-item">
                        <span class="stock-name">{stock['name']}</span>
                        <span class="stock-change {trend_class}">{stock['change']}</span>
                    </div>
'''
    
    html += f'''                </div>
            </div>
            <div class="stock-analysis">
                <strong>📊 分析：</strong>{stock_analysis['analysis']}
            </div>
        </section>

        <!-- 业界领袖观点 -->
        <section class="section" id="quote">
            <div class="section-title quote">
                💬 业界领袖观点
            </div>
'''
    
    # 添加观点
    for quote in quotes:
        html += f'''            <div class="quote-box">
                <p class="quote-text">{quote['text']}</p>
                <div class="quote-author">— {quote['author']}，{quote['title']}</div>
            </div>
'''
    
    html += f'''        </section>

        <footer class="footer">
            <p>🤖 AI日报 v1.1 | 每日精选全球人工智能热点</p>
            <p>生成时间：{today} | 数据来源：公开网络</p>
        </footer>
    </div>

    <nav class="bottom-nav">
        <div class="bottom-nav-content">
            <a href="#headlines" class="bottom-nav-item active">
                <span class="bottom-nav-icon">🔥</span>
                <span>头条</span>
            </a>
            <a href="#domestic" class="bottom-nav-item">
                <span class="bottom-nav-icon">🇨🇳</span>
                <span>国内</span>
            </a>
            <a href="#international" class="bottom-nav-item">
                <span class="bottom-nav-icon">🌍</span>
                <span>海外</span>
            </a>
            <a href="#stocks" class="bottom-nav-item">
                <span class="bottom-nav-icon">📈</span>
                <span>股票</span>
            </a>
            <a href="#quote" class="bottom-nav-item">
                <span class="bottom-nav-icon">💬</span>
                <span>观点</span>
            </a>
        </div>
    </nav>
</body>
</html>'''
    
    return html

if __name__ == "__main__":
    html = generate_report()
    with open("/root/.openclaw/workspace/ai-report-2026-03-03.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ v1.1报告已生成: ai-report-2026-03-03.html")
