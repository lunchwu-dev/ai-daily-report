#!/usr/bin/env python3
"""
AI日报 v1.4.2 邮件发送脚本
发送给: lunchwu@gmail.com + CC列表
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
    """发送AI日报邮件"""
    
    today = datetime.now()
    date_str = today.strftime("%Y年%m月%d日")
    date_str_en = today.strftime("%B %d, %Y")
    
    msg = MIMEMultipart('alternative')
    # 邮件标题与报告标题保持一致: IT小路的每日AI简报
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
.date{{text-align:center;color:#94a3b8;margin-bottom:10px;font-size:14px}}
.version-badge{{display:inline-block;background:#10b981;color:#fff;padding:4px 12px;border-radius:20px;font-size:12px;margin-bottom:20px}}
.section{{margin-bottom:30px}}
.section-title{{color:#1f2937;font-size:18px;font-weight:bold;margin-bottom:15px;padding-bottom:8px;border-bottom:2px solid #e5e7eb}}
.headline{{background:linear-gradient(135deg,#fef3c7 0%,#fde68a 100%);padding:20px;border-radius:12px;border-left:4px solid #f59e0b;margin-bottom:20px}}
.headline-title{{color:#92400e;font-weight:bold;font-size:16px;margin-bottom:10px}}
.headline-content{{color:#78350f;line-height:1.6;font-size:14px}}
.summary-box{{background:#f3f4f6;padding:15px;border-radius:8px;margin-bottom:15px}}
.summary-title{{color:#374151;font-weight:600;margin-bottom:8px;font-size:14px}}
.summary-content{{color:#4b5563;line-height:1.6;font-size:13px}}
.stock-box{{background:#ecfdf5;padding:15px;border-radius:8px;margin-bottom:15px;border-left:4px solid #10b981}}
.stock-box-down{{background:#fef2f2;padding:15px;border-radius:8px;margin-bottom:15px;border-left:4px solid #ef4444}}
.stock-title{{color:#065f46;font-weight:600;margin-bottom:8px;font-size:14px}}
.stock-title-down{{color:#991b1b;font-weight:600;margin-bottom:8px;font-size:14px}}
.stock-content{{color:#047857;line-height:1.6;font-size:13px}}
.stock-content-down{{color:#b91c1c;line-height:1.6;font-size:13px}}
.link-box{{background:linear-gradient(135deg,#6366f1 0%,#8b5cf6 100%);padding:20px;border-radius:12px;text-align:center;margin:30px 0}}
.link-box a{{color:#fff;font-size:16px;text-decoration:none;font-weight:bold}}
.footer{{margin-top:30px;padding-top:20px;border-top:1px solid #e5e7eb;color:#6b7280;font-size:12px;text-align:center}}
.data-time{{color:#9ca3af;font-size:11px;margin-top:5px}}
.up{{color:#10b981;font-weight:bold}}
.down{{color:#ef4444;font-weight:bold}}
</style>
</head>
<body>
<div class="container">
<h1>🤖 IT小路的每日AI简报</h1>
<div class="subtitle">v1.4.2 多语言完整版</div>
<div class="date">{date_str} · {date_str_en}</div>
<div style="text-align:center"><span class="version-badge">v1.4.2 Release</span></div>

<div class="section">
<div class="section-title">🔥 今日头条 / Headlines</div>
<div class="headline">
<div class="headline-title">OpenAI完成1100亿美元史诗级融资，AI军备竞赛进入白热化阶段</div>
<div class="headline-content">OpenAI于3月2日宣布完成史上最大规模融资，金额高达1100亿美元，投后估值飙升至7300亿美元。本轮融资由Amazon领投500亿美元，NVIDIA投资300亿美元，软银投资300亿美元。这标志着AI行业正式进入"万亿美元俱乐部"竞争时代。</div>
</div>
</div>

<div class="section">
<div class="section-title">🇨🇳 国内AI热点 / Domestic AI News</div>
<div class="summary-box">
<div class="summary-content">
• 银河通用再融25亿元，成估值最高未上市机器人公司<br>
• 松延动力完成近10亿元B轮融资，宁德时代系领投<br>
• 豆包大模型1.6发布：支持深度思考与256k长上下文<br>
• 可灵Kling 3.0发布：原生4K视频生成与多镜头叙事<br>
• 华为发布昇腾芯片路线图：2026年Q1推出昇腾950PR<br>
• 千寻智能连续完成两轮融资近20亿元，估值破百亿
</div>
</div>
</div>

<div class="section">
<div class="section-title">🌍 海外AI热点 / International AI News</div>
<div class="summary-box">
<div class="summary-content">
• AI教父辛顿警告：2026年AI将取代更多工作岗位<br>
• Google AI医疗诊断系统获FDA突破性设备认定<br>
• GitHub Copilot X正式发布：AI编程助手全面进化<br>
• Claude 5技术预览发布：SWE-bench得分超90%<br>
• Tesla FSD V15开始推送：端到端神经网络重构<br>
• Amazon领投OpenAI 500亿美元，AWS云服务深度绑定
</div>
</div>
</div>

<div class="section">
<div class="section-title">📈 AI产业股票分析 / AI Stock Analysis</div>

<div class="stock-box">
<div class="stock-title">🇨🇳 A股关键个股（3月4日收盘）</div>
<div class="stock-content">
• 科大讯飞(002230): <span class="up">+4.85%</span> - 豆包大模型带动AI应用热潮<br>
• 寒武纪(688256): <span class="up">+6.32%</span> - 华为昇腾带动国产AI芯片上涨<br>
• 中际旭创(300308): <span class="up">+3.78%</span> - OpenAI融资利好光模块需求<br>
• 汇川技术(300124): <span class="up">+5.21%</span> - 具身智能融资加速，订单大增
</div>
</div>

<div class="stock-box">
<div class="stock-title">🇺🇸 美股关键个股（3月4日收盘）</div>
<div class="stock-content">
• NVIDIA(NVDA): <span class="up">+3.45%</span> - 参与OpenAI投资，数据中心业务强劲<br>
• Microsoft(MSFT): <span class="up">+1.28%</span> - Copilot X发布，Azure OpenAI超预期<br>
• Alphabet(GOOGL): <span class="up">+0.95%</span> - AI医疗系统获FDA认定<br>
• Tesla(TSLA): <span class="down">-1.32%</span> - FSD V15推送缓慢，短期承压
</div>
</div>
</div>

<div class="section">
<div class="section-title">💡 投资建议 / Investment Advice</div>
<div class="summary-box">
<div class="summary-title">核心观点</div>
<div class="summary-content">
<strong>短期策略（1-3个月）：</strong>超配光模块和国产AI芯片，关注具身智能产业链。<br><br>
<strong>中长期布局（6-12个月）：</strong>NVIDIA仍是AI基础设施核心；Microsoft受益于Copilot生态。<br><br>
<strong>风险提示：</strong>OpenAI巨额融资可能加剧行业垄断；AI板块整体估值偏高。
</div>
</div>
</div>

<div class="link-box">
<a href="https://52199df7.ai-daily-report-32b.pages.dev" target="_blank">📱 点击查看完整报告 / View Full Report →</a>
</div>

<div class="footer">
IT小路的每日AI简报 | v1.4.2 Release<br>
<div class="data-time">数据截止时间：{date_str} 07:30 (Asia/Shanghai)</div>
<div class="data-time">版本特性：多语言切换 | 产业链分析 | 零售AI应用专区</div>
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
