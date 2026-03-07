#!/usr/bin/env python3
"""
AI日报 v1.6.1 邮件发送脚本 - 精简版
发送给: lunchwu@gmail.com + CC列表
邮件正文: 中英文小结 + 完整报告链接
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# 邮件配置
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
SENDER_EMAIL = 'lunchwu@gmail.com'
SENDER_PASSWORD = 'bize wlmw kupz jnoc'  # Gmail应用密码

# 收件人配置
PRIMARY_RECIPIENT = 'lunchwu@gmail.com'
CC_RECIPIENTS = [
    'jerry.wu1@decathlon.com',
    'leanna.li@decathlon.com',
    'tia.song@decathlon.com'
]

def send_daily_report():
    """发送AI日报邮件 - 精简版（中英文小结+链接）"""
    
    today = datetime.now()
    date_str = today.strftime("%Y年%m月%d日")
    date_str_en = today.strftime("%B %d, %Y")
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'🤖 IT小路的每日AI简报 | {date_str}'
    msg['From'] = SENDER_EMAIL
    msg['To'] = PRIMARY_RECIPIENT
    msg['Cc'] = ', '.join(CC_RECIPIENTS)
    
    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f8fafc;padding:20px}}
.container{{max-width:700px;margin:0 auto;background:#fff;border-radius:16px;padding:40px;box-shadow:0 4px 6px rgba(0,0,0,0.1)}}
h1{{color:#6366f1;text-align:center;margin-bottom:10px;font-size:28px}}
.subtitle{{text-align:center;color:#64748b;margin-bottom:5px;font-size:16px}}
.date{{text-align:center;color:#94a3b8;margin-bottom:20px;font-size:14px}}
.section{{margin-bottom:30px}}
.section-title{{color:#1f2937;font-size:18px;font-weight:bold;margin-bottom:15px;padding-bottom:8px;border-bottom:2px solid #e5e7eb}}
.summary-content{{color:#374151;line-height:1.8;font-size:14px}}
.summary-content p{{margin-bottom:12px}}
.link-box{{background:linear-gradient(135deg,#6366f1 0%,#8b5cf6 100%);padding:20px;border-radius:12px;text-align:center;margin:30px 0}}
.link-box a{{color:#fff;font-size:16px;text-decoration:none;font-weight:bold}}
.footer{{margin-top:30px;padding-top:20px;border-top:1px solid #e5e7eb;color:#6b7280;font-size:12px;text-align:center}}
.data-time{{color:#9ca3af;font-size:11px;margin-top:5px}}
</style>
</head>
<body>
<div class="container">
<h1>🤖 IT小路的每日AI简报</h1>
<div class="subtitle">AI Daily Briefing</div>
<div class="date">{date_str} · {date_str_en}</div>

<div class="section">
<div class="section-title">📋 中文小结 / Chinese Summary</div>
<div class="summary-content">
<p><strong>🔥 今日头条：</strong>两会聚焦AI，工信部部长宣布推动人工智能与制造业"双向奔赴"。2025年我国AI核心产业规模超1.2万亿元，企业数量超6200家。</p>
<p><strong>🇨🇳 国内热点：</strong>阿里通义千问技术负责人离职；特斯拉中国与火山引擎合作；清华系机器人企业获大额融资，2026年人形机器人融资突破130亿元。</p>
<p><strong>🌍 海外热点：</strong>Google DeepMind发布AI编程代理AlphaEvolve；OpenAI GPT-5预览版发布；Anthropic Claude 4发布。</p>
<p><strong>📈 AI股票：</strong>美股周五芯片股普跌，NVIDIA -4.16%、AMD -2.30%受出口管制担忧影响；A股国产AI芯片上涨，寒武纪 +6.32%、科大讯飞 +4.85%受益于国产替代政策。</p>
<p><strong>💡 投资建议：</strong>短期关注国产AI芯片替代逻辑；中长期NVIDIA仍是AI基础设施核心，但需关注地缘政治风险。</p>
</div>
</div>

<div class="section">
<div class="section-title">📋 English Summary</div>
<div class="summary-content">
<p><strong>🔥 Headlines:</strong> China's Two Sessions focus on AI. MIIT announces push for AI-manufacturing integration. China's AI core industry exceeded 1.2 trillion yuan in 2025.</p>
<p><strong>🇨🇳 Domestic:</strong> Alibaba Tongyi Qianwen tech lead departs; Tesla China partners with ByteDance; Tsinghua robotics firms secure funding.</p>
<p><strong>🌍 International:</strong> Google DeepMind releases AlphaEvolve coding agent; OpenAI GPT-5 preview; Anthropic Claude 4 launch.</p>
<p><strong>📈 AI Stocks:</strong> US chip stocks declined Friday. NVIDIA -4.16%, AMD -2.30% on export control concerns. A-share domestic AI chips rose. Cambricon +6.32%, iFlytek +4.85% on substitution benefits.</p>
<p><strong>💡 Investment:</strong> Short-term focus on domestic AI chip substitution. Long-term NVIDIA remains core AI infrastructure, but geopolitical risks need attention.</p>
</div>
</div>

<div class="link-box">
<a href="https://cc7fb1a3.ai-daily-report-32b.pages.dev" target="_blank">📱 点击查看完整报告 / View Full Report →</a>
</div>

<div class="footer">
IT小路的每日AI简报 | AI Daily Briefing<br>
<div class="data-time">数据截止 / Data cutoff: {date_str} 07:15 (Asia/Shanghai)</div>
<div class="data-time">v1.6.1 Release · 实时数据驱动 / Real-time Data Powered</div>
</div>
</div>
</body>
</html>'''
    
    msg.attach(MIMEText(html, 'html', 'utf-8'))
    
    # 所有收件人（主收件人 + CC）
    all_recipients = [PRIMARY_RECIPIENT] + CC_RECIPIENTS
    
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, all_recipients, msg.as_string())
        server.quit()
        print('✅ 邮件发送成功')
        print(f'   主收件人: {PRIMARY_RECIPIENT}')
        print(f'   CC: {", ".join(CC_RECIPIENTS)}')
        return True
    except Exception as e:
        print(f'❌ 邮件发送失败: {e}')
        return False

if __name__ == '__main__':
    send_daily_report()
