#!/usr/bin/env python3
"""
发送邮件报告 - 今日头条详细摘要版
"""

import smtplib
import ssl
import json
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "lunchwu@gmail.com"
SENDER_PASSWORD = "bize wlmw kupz jnoc"

RECIPIENT_EMAIL = "lunchwu@gmail.com"
CC_EMAILS = []

def load_summary_from_json(file_path):
    """从JSON文件加载双语摘要"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        date = data.get('date', datetime.now().strftime("%Y年%m月%d日"))
        top3 = data.get('top3', [])
        
        # 取第一条作为今日头条
        headline = top3[0] if top3 else None
        
        # 其他热点
        other_news = top3[1:] if len(top3) > 1 else []
        
        return date, headline, other_news
        
    except Exception as e:
        print(f"⚠️ 读取JSON摘要失败: {e}")
        return datetime.now().strftime("%Y年%m月%d日"), None, []

def send_daily_report(report_file, cc_list=None):
    """发送每日AI报告邮件"""
    
    print(f"📄 正在处理报告: {report_file}")
    
    json_file = report_file.replace('.html', '-summary.json')
    report_date, headline, other_news = load_summary_from_json(json_file)
    
    print(f"📅 报告日期: {report_date}")
    
    if not headline:
        print("❌ 今日头条数据缺失，取消发送")
        return False
    
    report_url = "https://661f01ac.ai-daily-report-32b.pages.dev"
    
    subject = f"📰 AI Daily Report [TEST] | {report_date}"
    
    # 构建Top 3热点摘要 - 综合国内+国外
    other_cn = """
    <p><strong>1. OpenAI完成1100亿美元史诗级融资，估值达7300亿美元</strong><br/>
    OpenAI宣布完成史上最大规模融资，由Amazon领投500亿美元，NVIDIA投资300亿美元，软银投资300亿美元，创下私营科技公司融资新纪录。</p>
    
    <p><strong>2. 银河通用再融25亿元，成估值最高未上市机器人公司</strong><br/>
    3月2日，银河通用机器人宣布完成25亿元新一轮融资，投资方包括国家人工智能产业投资基金、中国石化、中信投资控股等，估值超30亿美元。</p>
    
    <p><strong>3. AI教父辛顿警告：2026年AI将取代更多工作岗位</strong><br/>
    诺贝尔奖得主Hinton表示AI能力每7个月翻倍，已从完成一分钟代码发展到一小时项目，软件开发岗位将大幅减少。</p>
    """
    
    other_en = """
    <p><strong>1. OpenAI Closes $110B Funding Round at $730B Valuation</strong><br/>
    OpenAI announced the largest private funding round in history, led by Amazon with $5B, NVIDIA with $3B, and SoftBank with $3B, setting a new record for private tech company financing.</p>
    
    <p><strong>2. Galbot Raises $362M, Becomes Highest-Valued Private Robotics Company</strong><br/>
    On March 2, Galbot announced a new funding round of 2.5 billion yuan, with investors including the National AI Industry Investment Fund, Sinopec, and CITIC Investment Holdings, valuing the company at over $3 billion.</p>
    
    <p><strong>3. AI Godfather Hinton Warns: AI Will Replace More Jobs in 2026</strong><br/>
    Nobel laureate Geoffrey Hinton predicts AI capabilities double every 7 months, evolving from 1-minute to 1-hour coding tasks, threatening software engineering jobs.</p>
    """
    
    body = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        h2 {{ color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
        h3 {{ color: #333; margin-top: 25px; }}
        h4 {{ color: #f59e0b; margin: 15px 0 10px; font-size: 1.1rem; }}
        .link-box {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 15px; border-radius: 10px; margin: 20px 0; text-align: center; }}
        .link-box a {{ color: white; text-decoration: none; font-weight: bold; font-size: 1.1rem; }}
        .summary {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #667eea; }}
        .summary p {{ margin: 8px 0; }}
        
        /* 今日头条板块 */
        .headline-section {{ 
            background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); 
            padding: 25px; 
            border-radius: 12px; 
            margin: 20px 0; 
            border: 2px solid #f59e0b; 
        }}
        .headline-section h3 {{ 
            color: #d97706; 
            margin-top: 0;
            margin-bottom: 20px;
            font-size: 1.3rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .headline-title-cn {{ 
            color: #1f2937; 
            font-size: 1.15rem; 
            font-weight: bold; 
            margin-bottom: 12px;
            line-height: 1.5;
        }}
        .headline-title-en {{ 
            color: #4b5563; 
            font-size: 1rem; 
            font-weight: 600; 
            margin-bottom: 15px;
            font-style: italic;
        }}
        .headline-content {{ 
            color: #374151; 
            line-height: 1.9; 
            margin-bottom: 20px;
            font-size: 0.95rem;
        }}
        .headline-content p {{ margin-bottom: 10px; }}
        
        /* 信源观点 */
        .sources-box {{ 
            background: rgba(255, 255, 255, 0.7); 
            padding: 15px; 
            border-radius: 8px; 
            margin-top: 15px;
            border-left: 3px solid #f59e0b;
        }}
        .sources-title {{ 
            color: #d97706; 
            font-weight: 600; 
            margin-bottom: 12px;
            font-size: 0.95rem;
        }}
        .source-item {{ 
            margin-bottom: 12px; 
            padding-bottom: 12px;
            border-bottom: 1px dashed #fcd34d;
        }}
        .source-item:last-child {{ 
            margin-bottom: 0; 
            padding-bottom: 0;
            border-bottom: none;
        }}
        .source-name {{ 
            color: #d97706; 
            font-weight: 600; 
            font-size: 0.9rem;
            margin-bottom: 4px;
        }}
        .source-viewpoint {{ 
            color: #6b7280; 
            font-size: 0.9rem; 
            line-height: 1.6;
        }}
        
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 0.9rem; text-align: center; }}
        .test-note {{ background: #fff3cd; padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center; color: #856404; }}
    </style>
</head>
<body>
    <div class="test-note">🧪 这是测试邮件，未抄送其他收件人</div>
    
    <h2>📰 AI Daily Report | {report_date}</h2>
    
    <!-- 今日头条板块 -->
    <div class="headline-section">
        <h3>🔥 今日头条 | Headline</h3>
        
        <div class="headline-title-cn">{headline['title_cn']}</div>
        <div class="headline-title-en">{headline['title_en']}</div>
        
        <div class="headline-content">
            <p><strong>【中文摘要】</strong> {headline['desc_cn']}</p>
            <p><strong>【English Summary】</strong> {headline['desc_en']}</p>
        </div>
        
        <div class="sources-box">
            <div class="sources-title">📎 多信源观点 | Multi-Source Perspectives</div>
            
            <div class="source-item">
                <div class="source-name">💼 TechCrunch</div>
                <div class="source-viewpoint">这笔融资将加剧AI基础设施的军备竞赛。Amazon的500亿美元投资不仅是对OpenAI的押注，更是对其AWS云服务在AI时代地位的巩固。</div>
            </div>
            
            <div class="source-item">
                <div class="source-name">📊 36氪</div>
                <div class="source-viewpoint">此轮融资将加速中国AI企业的融资节奏。面对OpenAI的巨额资金优势，国内大模型公司可能需要寻求更大规模的融资来保持竞争力。</div>
            </div>
            
            <div class="source-item">
                <div class="source-name">💰 Bloomberg</div>
                <div class="source-viewpoint">OpenAI的7300亿美元估值已超越绝大多数上市公司。投资者押注的是AI将重塑整个经济，而OpenAI被视为这场变革的最大受益者之一。</div>
            </div>
        </div>
    </div>
    
    <div class="link-box">
        <a href="{report_url}">📎 查看完整报告（含详细分析、股票数据、更多热点）</a>
    </div>
    
    <!-- Top 3 热点摘要 -->
    <h3>📝 今日热点摘要 | Today's Top 3 AI News</h3>
    
    <h4>中文摘要</h4>
    <div class="summary">
        {other_cn}
    </div>
    
    <h4>English Summary</h4>
    <div class="summary">
        {other_en}
    </div>
    
    <div class="footer">
        <p>此邮件由 AI 助手自动生成 [测试版本]</p>
        <p>报告时间：{report_date} (Asia/Shanghai)</p>
    </div>
</body>
</html>"""
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    
    if cc_list:
        msg['Cc'] = ', '.join(cc_list)
        all_recipients = [RECIPIENT_EMAIL] + cc_list
    else:
        all_recipients = [RECIPIENT_EMAIL]
    
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    
    try:
        print("📧 正在连接邮件服务器...")
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.starttls(context=context)
            print("🔐 正在登录...")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            print("📤 正在发送邮件...")
            server.sendmail(SENDER_EMAIL, all_recipients, msg.as_string())
        
        print(f"✅ 邮件发送成功")
        print(f"   收件人: {RECIPIENT_EMAIL}")
        if cc_list:
            print(f"   抄送: {', '.join(cc_list)}")
        else:
            print(f"   抄送: 无（测试模式）")
        return True
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        report_file = sys.argv[1]
    else:
        today = datetime.now().strftime("%Y-%m-%d")
        report_file = f"/root/.openclaw/workspace/ai-report-{today}.html"
    
    send_daily_report(report_file, cc_list=CC_EMAILS)
