#!/usr/bin/env python3
"""
AI日报 v1.6.1 邮件发送脚本 - 测试版（仅发送给主收件人）
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# 邮件配置
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
SENDER_EMAIL = 'lunchwu@gmail.com'
SENDER_PASSWORD = 'bize wlmw kupz jnoc'

# 仅发送给主收件人（测试）
RECIPIENT = 'lunchwu@gmail.com'

def send_test_email():
    """发送测试邮件"""
    
    today = datetime.now()
    date_str = today.strftime("%Y年%m月%d日")
    date_str_en = today.strftime("%B %d, %Y")
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'🤖 IT小路的每日AI简报 | {date_str} [测试邮件]'
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT
    
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
.test-badge{{display:inline-block;background:#f59e0b;color:#fff;padding:4px 12px;border-radius:20px;font-size:12px;margin-bottom:20px}}
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
<div style="text-align:center"><span class="test-badge">🧪 测试邮件 Test Email</span></div>

<div class="section">
<div class="section-title">📋 中文小结 / Chinese Summary</div>
<div class="summary-content">
<p><strong>🔥 今日头条：</strong>两会聚焦AI，工信部部长宣布推动人工智能与制造业"双向奔赴"。2025年我国AI核心产业规模超1.2万亿元，企业数量超6200家。</p>
<p><strong>🇨🇳 国内热点：</strong>阿里通义千问技术负责人林俊旸离职；特斯拉中国与火山引擎合作，Model Y L将搭载豆包大模型；清华系机器人企业星动纪元、极佳视界同日获大额融资，2026年人形机器人融资突破130亿元。</p>
<p><strong>🌍 海外热点：</strong>Google DeepMind发布AI编程代理AlphaEvolve；OpenAI GPT-5预览版发布，多模态能力大幅提升；Anthropic Claude 4发布，推理能力超越GPT-4。</p>
<p><strong>📈 AI股票：</strong>美股周五芯片股普跌，NVIDIA -4.16%、AMD -2.30%受美国AI芯片出口管制新规担忧影响；A股国产AI芯片逆势上涨，寒武纪 +6.32%、科大讯飞 +4.85%、海光信息 +3.45%受益于国产替代加速政策。</p>
<p><strong>💡 投资建议：</strong>短期超配国产AI芯片（寒武纪、海光）受益于替代逻辑；中长期NVIDIA仍是AI基础设施核心，但需关注地缘政治风险；全球配置建议基础设施40%、模型层30%、应用层30%。</p>
</div>
</div>

<div class="section">
<div class="section-title">📋 English Summary</div>
<div class="summary-content">
<p><strong>🔥 Headlines:</strong> China's Two Sessions focus on AI. MIIT Minister Li Lecheng announces push for AI-manufacturing integration. China's AI core industry exceeded 1.2 trillion yuan in 2025 with 6,200+ companies.</p>
<p><strong>🇨🇳 Domestic:</strong> Alibaba Tongyi Qianwen tech lead Lin Junyang departs; Tesla China partners with ByteDance's Volcano Engine; Tsinghua robotics firms Star1 AI and Jishi Vision secure major funding.</p>
<p><strong>🌍 International:</strong> Google DeepMind releases AlphaEvolve coding agent; OpenAI GPT-5 preview launched with improved multimodal capabilities; Anthropic Claude 4 released with enhanced reasoning.</p>
<p><strong>📈 AI Stocks:</strong> US chip stocks declined Friday on export control concerns. NVIDIA -4.16%, AMD -2.30%. A-share domestic AI chips rose. Cambricon +6.32%, iFlytek +4.85%, Hygon +3.45% on substitution benefits.</p>
<p><strong>💡 Investment:</strong> Short-term overweight domestic AI chips. Long-term NVIDIA remains core AI infrastructure. Global allocation: Infrastructure 40%, Model 30%, Application 30%.</p>
</div>
</div>

<div class="link-box">
<a href="https://cc7fb1a3.ai-daily-report-32b.pages.dev" target="_blank">📱 点击查看完整报告 / View Full Report →</a>
</div>

<div class="footer">
IT小路的每日AI简报 | AI Daily Briefing<br>
<div class="data-time">数据截止 / Data cutoff: {date_str} 07:15 (Asia/Shanghai)</div>
<div class="data-time">v1.6.1 Release · 实时数据驱动 / Real-time Data Powered</div>
<div class="data-time" style="color:#f59e0b;margin-top:10px;">🧪 这是测试邮件，仅发送给主收件人 / This is a test email sent to primary recipient only</div>
</div>
</div>
</body>
</html>'''
    
    msg.attach(MIMEText(html, 'html', 'utf-8'))
    
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, [RECIPIENT], msg.as_string())
        server.quit()
        print('✅ 测试邮件发送成功')
        print(f'   收件人: {RECIPIENT}')
        return True
    except Exception as e:
        print(f'❌ 邮件发送失败: {e}')
        return False

if __name__ == '__main__':
    send_test_email()
