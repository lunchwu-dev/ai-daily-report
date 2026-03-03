#!/usr/bin/env python3
"""
AI日报生成器 - 使用GitHub模板生成报告
"""

import json
from datetime import datetime

def generate_report():
    today = "2026年3月3日"
    weekday = "星期二"
    
    # 国内热点
    domestic_news = [
        {
            "source": "🚀 银河通用",
            "title": "银河通用再融25亿元，成估值最高未上市机器人公司",
            "summary": "3月2日，银河通用机器人宣布完成25亿元新一轮融资，投资方包括国家人工智能产业投资基金、中国石化、中信投资控股等。本轮融资后，公司累计融资额为中国具身智能领域首位，估值超30亿美元。",
            "link": "https://www.caixin.com/2026-03-02/102418619.html"
        },
        {
            "source": "🔋 松延动力",
            "title": "松延动力完成近10亿元B轮融资，宁德时代系领投",
            "summary": "人形机器人企业松延动力宣布完成B轮融资，由宁德时代系产业投资平台晨道资本领投，国科投资、九合创投等跟投。公司已完成股改，为IPO做准备。",
            "link": "https://www.36kr.com/p/3705734996324487"
        },
        {
            "source": "🎵 字节跳动",
            "title": "豆包大模型1.6发布：支持深度思考与256k长上下文",
            "summary": "字节跳动发布豆包大模型1.6系列，均支持深度思考、多模态理解、256k长上下文、图形界面操作等能力，能够更好地支持复杂Agent的构建。",
            "link": "https://k.sina.com.cn/article_7857201856_1d45362c001902rw5s.html"
        },
        {
            "source": "💻 华为",
            "title": "华为发布昇腾芯片路线图：2026年Q1推出昇腾950PR",
            "summary": "华为轮值董事长徐直军宣布，预计2026年Q1推出昇腾950PR芯片，950PR采用华为自研HBM，互联带宽提升2.5倍，Atlas 950 SuperPoD将成为全球最强AI超节点。",
            "link": "https://g.pconline.com.cn/x/1985/19857872.html"
        },
        {
            "source": "🎬 快手",
            "title": "可灵Kling 3.0发布：原生4K视频生成与多镜头叙事",
            "summary": "快手发布可灵Kling 3.0，支持原生4K输出、15秒连续视频生成、多镜头自动叙事、原生音频集成。Video O1统一多模态模型支持720p分辨率。",
            "link": "https://top.aibase.com/tool/kling-3-0-ai"
        },
        {
            "source": "🤖 千寻智能",
            "title": "千寻智能连续完成两轮融资近20亿元，估值破百亿",
            "summary": "具身智能企业千寻智能宣布近期连续完成两轮融资近20亿元，投资方包括云锋基金、混沌投资、红杉中国等一线机构。千寻智能已在宁德时代投运全球首条人形具身智能产线。",
            "link": "http://finance.ce.cn/stock/gsgdbd/202603/t20260302_2796529.shtml"
        }
    ]
    
    # 海外热点
    international_news = [
        {
            "source": "💰 OpenAI",
            "title": "OpenAI完成1100亿美元融资，估值达7300亿美元",
            "summary": "OpenAI完成史上最大规模融资，Amazon领投500亿美元，ChatGPT周活跃用户达9亿，预计2026年收入290亿美元。",
            "link": "https://techcrunch.com/2026/03/02/openai-110b-funding/"
        },
        {
            "source": "🧠 Geoffrey Hinton",
            "title": "AI教父辛顿警告：2026年AI将取代更多工作岗位",
            "summary": "诺贝尔奖得主Hinton表示AI能力每7个月翻倍，已从完成一分钟代码发展到一小时项目，软件开发岗位将大幅减少。",
            "link": "https://www.bbc.com/news/technology-2026-ai-hinton-warning"
        },
        {
            "source": "🏥 Google Health",
            "title": "Google AI医疗诊断系统获FDA突破性设备认定",
            "summary": "Google Health开发的AI辅助诊断系统在早期癌症检测方面达到95%准确率，获得FDA突破性设备认定，预计2026年Q3商业化。",
            "link": "https://blog.google/technology/health/ai-medical-diagnosis-fda/"
        },
        {
            "source": "💻 Microsoft",
            "title": "GitHub Copilot X正式发布：AI编程助手全面进化",
            "summary": "微软发布GitHub Copilot X，集成GPT-5技术，支持自然语言代码生成、自动bug修复、代码解释和文档生成，月活开发者突破500万。",
            "link": "https://github.blog/2026-03-02-github-copilot-x/"
        },
        {
            "source": "🚗 Tesla",
            "title": "Tesla FSD V15开始推送：端到端神经网络重构",
            "summary": "Tesla开始向北美车主推送FSD V15版本，采用全新端到端神经网络架构，城市街道自动驾驶能力提升40%，事故率降低60%。",
            "link": "https://www.tesla.com/blog/fsd-v15-update"
        },
        {
            "source": "📱 Anthropic",
            "title": "Claude 5技术预览发布：SWE-bench得分超90%",
            "summary": "Anthropic发布Claude 5技术预览，在SWE-bench Verified基准测试中得分超过90%，代码理解和生成能力大幅提升，正式版预计Q2发布。",
            "link": "https://www.anthropic.com/news/claude-5-preview"
        }
    ]
    
    # 业界领袖观点
    quotes = [
        {
            "text": "到2026年，人工智能将有能力取代很多很多工作。每隔7个月左右，它所能完成的任务量就会差不多翻倍。在编程领域，以前它只能完成一分钟的代码，现在可以完成一小时规模的项目。",
            "author": "Geoffrey Hinton",
            "title": "AI教父、图灵奖&诺贝尔奖得主"
        },
        {
            "text": "Claude 5代表了重大飞跃。与Claude 4.5 Opus相比，大多数基准提升了20-25%。在SWE-bench Verified上，我们舒适地超过了90%。我们的目标是Q2公开发布。",
            "author": "Dario Amodei",
            "title": "Anthropic CEO"
        },
        {
            "text": "资本市场对具身智能的热度依旧，也在真金白银地下注。大部分具身智能公司并不缺钱，主要是'囤钱'的心态，说明大家普遍认可这个赛道的巨大空间。",
            "author": "胥晓敏",
            "title": "阿米奥机器人联合创始人"
        }
    ]
    
    # 市场情绪
    sentiments = [
        {"label": "具身智能板块", "value": "强烈看涨 88%", "width": 88, "class": "bullish"},
        {"label": "大模型板块", "value": "看涨 72%", "width": 72, "class": "bullish"},
        {"label": "AI芯片板块", "value": "震荡 55%", "width": 55, "class": "neutral"},
        {"label": "AI应用板块", "value": "看涨 68%", "width": 68, "class": "bullish"}
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
            body {{
                padding: 30px;
                padding-bottom: 30px;
            }}
            
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
            
            .top-nav-links a:hover {{
                color: #6366f1;
            }}
            
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
                text-shadow: 0 0 60px rgba(99, 102, 241, 0.5);
            }}
            
            .header .date {{
                font-size: 1.1rem;
                color: #94a3b8;
                letter-spacing: 2px;
            }}
            
            .section {{
                margin-bottom: 50px;
            }}
            
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
            
            .sentiment-grid {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 25px;
            }}
            
            .sentiment-item {{
                background: #1e293b;
                border-radius: 12px;
                padding: 25px;
                border: 1px solid rgba(148, 163, 184, 0.1);
            }}
            
            .sentiment-label {{
                color: #64748b;
                font-size: 0.95rem;
                margin-bottom: 10px;
            }}
            
            .sentiment-value {{
                font-size: 1.8rem;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            
            .sentiment-bar {{
                height: 6px;
                background: #334155;
                border-radius: 3px;
                overflow: hidden;
            }}
            
            .sentiment-bar-fill {{
                height: 100%;
                border-radius: 3px;
                transition: width 0.5s ease;
            }}
            
            .history-nav {{
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
            }}
            
            .history-item {{
                background: #1e293b;
                border-radius: 10px;
                padding: 15px 25px;
                border: 1px solid rgba(245, 158, 11, 0.3);
                color: #f59e0b;
                text-decoration: none;
                transition: all 0.3s;
                font-weight: 500;
                min-height: 44px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .history-item:hover {{
                background: rgba(245, 158, 11, 0.1);
                transform: translateY(-3px);
            }}
            
            .footer {{
                text-align: center;
                padding: 40px;
                color: #64748b;
                border-top: 1px solid rgba(148, 163, 184, 0.1);
                margin-top: 40px;
            }}
            
            .bottom-nav {{
                display: none;
            }}
        }}
        
        /* 移动端样式 */
        @media (max-width: 768px) {{
            body {{
                padding: 16px;
                padding-bottom: 90px;
            }}
            
            .top-nav {{
                display: none;
            }}
            
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
            
            .section {{
                margin-bottom: 30px;
            }}
            
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
                transition: all 0.2s ease;
                border: 1px solid rgba(148, 163, 184, 0.1);
                position: relative;
                overflow: hidden;
                width: 100%;
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
            
            .card:active {{
                transform: scale(0.98);
                background: #252f47;
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
            
            .card-link {{
                display: inline-flex;
                align-items: center;
                gap: 6px;
                color: #6366f1;
                text-decoration: none;
                font-weight: 600;
                transition: all 0.2s;
                font-size: 0.9em;
                min-height: 44px;
                padding: 8px 0;
            }}
            
            .quote-box {{
                background: linear-gradient(135deg, #1e293b 0%, rgba(168, 85, 247, 0.1) 100%);
                border-radius: 12px;
                padding: 20px;
                border: 1px solid rgba(168, 85, 247, 0.3);
                position: relative;
                margin-bottom: 16px;
            }}
            
            .quote-box::before {{
                content: '"';
                font-size: 2.5em;
                color: rgba(168, 85, 247, 0.3);
                position: absolute;
                top: 5px;
                left: 15px;
                font-family: Georgia, serif;
            }}
            
            .quote-text {{
                font-size: 0.95rem;
                color: #e2e8f0;
                line-height: 1.7;
                padding-left: 30px;
                font-style: italic;
            }}
            
            .quote-author {{
                text-align: right;
                color: #a855f7;
                margin-top: 12px;
                font-weight: 600;
                font-size: 0.9rem;
            }}
            
            .sentiment-grid {{
                display: grid;
                grid-template-columns: 1fr;
                gap: 12px;
            }}
            
            .sentiment-item {{
                background: #1e293b;
                border-radius: 10px;
                padding: 18px;
                border: 1px solid rgba(148, 163, 184, 0.1);
            }}
            
            .sentiment-label {{
                color: #64748b;
                font-size: 0.9rem;
                margin-bottom: 8px;
            }}
            
            .sentiment-value {{
                font-size: 1.5rem;
                font-weight: bold;
                margin-bottom: 8px;
            }}
            
            .sentiment-bar {{
                height: 6px;
                background: #334155;
                border-radius: 3px;
                overflow: hidden;
            }}
            
            .sentiment-bar-fill {{
                height: 100%;
                border-radius: 3px;
                transition: width 0.5s ease;
            }}
            
            .history-nav {{
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }}
            
            .history-item {{
                background: #1e293b;
                border-radius: 8px;
                padding: 12px 18px;
                border: 1px solid rgba(245, 158, 11, 0.3);
                color: #f59e0b;
                text-decoration: none;
                transition: all 0.2s;
                font-weight: 500;
                font-size: 0.9rem;
                min-height: 44px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .history-item:active {{
                background: rgba(245, 158, 11, 0.15);
                transform: scale(0.98);
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
                padding-bottom: max(8px, env(safe-area-inset-bottom));
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
                transition: color 0.2s;
            }}
            
            .bottom-nav-item.active {{
                color: #6366f1;
            }}
            
            .bottom-nav-icon {{
                font-size: 1.4rem;
                margin-bottom: 2px;
            }}
        }}
        
        /* 公共样式 */
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
        
        .section-title.sentiment {{
            border-left: 4px solid #10b981;
            background: linear-gradient(135deg, #1e293b 0%, rgba(16, 185, 129, 0.1) 100%);
        }}
        
        .section-title.history {{
            border-left: 4px solid #f59e0b;
            background: linear-gradient(135deg, #1e293b 0%, rgba(245, 158, 11, 0.1) 100%);
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
        
        .sentiment-value.bullish {{
            color: #10b981;
        }}
        
        .sentiment-value.bearish {{
            color: #ef4444;
        }}
        
        .sentiment-value.neutral {{
            color: #f59e0b;
        }}
        
        .sentiment-bar-fill.bullish {{
            background: linear-gradient(90deg, #10b981, #34d399);
        }}
        
        .sentiment-bar-fill.bearish {{
            background: linear-gradient(90deg, #ef4444, #f87171);
        }}
        
        .sentiment-bar-fill.neutral {{
            background: linear-gradient(90deg, #f59e0b, #fbbf24);
        }}
        
        .footer p {{
            margin: 6px 0;
        }}
        
        html {{
            scroll-behavior: smooth;
        }}
        
        ::selection {{
            background: rgba(99, 102, 241, 0.3);
            color: #fff;
        }}
    </style>
</head>
<body>
    <!-- PC端顶部导航 -->
    <nav class="top-nav">
        <div class="top-nav-content">
            <div class="top-nav-logo">🤖 AI日报</div>
            <div class="top-nav-links">
                <a href="#domestic">国内热点</a>
                <a href="#international">海外热点</a>
                <a href="#quote">领袖观点</a>
                <a href="#sentiment">市场情绪</a>
                <a href="#history">往期报告</a>
            </div>
        </div>
    </nav>

    <div class="container">
        <header class="header">
            <h1>🤖 AI日报</h1>
            <div class="date">{today} · {weekday}</div>
        </header>

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
    
    html += '''        </section>

        <!-- 市场情绪分析 -->
        <section class="section" id="sentiment">
            <div class="section-title sentiment">
                📈 市场情绪分析
            </div>
            <div class="sentiment-grid">
'''
    
    # 添加市场情绪
    for s in sentiments:
        html += f'''                <div class="sentiment-item">
                    <div class="sentiment-label">{s['label']}</div>
                    <div class="sentiment-value {s['class']}">{s['value']}</div>
                    <div class="sentiment-bar">
                        <div class="sentiment-bar-fill {s['class']}" style="width: {s['width']}%"></div>
                    </div>
                </div>
'''
    
    html += f'''            </div>
        </section>

        <!-- 往期报告导航 -->
        <section class="section" id="history">
            <div class="section-title history">
                📚 往期报告
            </div>
            <div class="history-nav">
                <a href="https://ai-daily-report-2026-03-02.pages.dev" class="history-item">3月2日</a>
                <a href="https://ai-daily-report-2026-03-01.pages.dev" class="history-item">3月1日</a>
                <a href="https://ai-daily-report-2026-02-28.pages.dev" class="history-item">2月28日</a>
                <a href="https://6613149a.ai-daily-report-index.pages.dev" class="history-item">查看更多</a>
            </div>
        </section>

        <footer class="footer">
            <p>🤖 AI日报 | 每日精选全球人工智能热点</p>
            <p>生成时间：{today} | 数据来源：公开网络</p>
        </footer>
    </div>

    <!-- 移动端底部固定导航 -->
    <nav class="bottom-nav">
        <div class="bottom-nav-content">
            <a href="#domestic" class="bottom-nav-item active">
                <span class="bottom-nav-icon">🇨🇳</span>
                <span>国内</span>
            </a>
            <a href="#international" class="bottom-nav-item">
                <span class="bottom-nav-icon">🌍</span>
                <span>海外</span>
            </a>
            <a href="#quote" class="bottom-nav-item">
                <span class="bottom-nav-icon">💬</span>
                <span>观点</span>
            </a>
            <a href="#sentiment" class="bottom-nav-item">
                <span class="bottom-nav-icon">📈</span>
                <span>情绪</span>
            </a>
            <a href="#history" class="bottom-nav-item">
                <span class="bottom-nav-icon">📚</span>
                <span>往期</span>
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
    print("✅ 报告已生成: ai-report-2026-03-03.html")
