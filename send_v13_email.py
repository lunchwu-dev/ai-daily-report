#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

msg = MIMEMultipart('alternative')
msg['Subject'] = '🤖 AI日报 v1.3 - 2026年3月3日'
msg['From'] = 'lunchwu@gmail.com'
msg['To'] = 'lunchwu@gmail.com'

html = '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f8fafc;padding:20px}
.container{max-width:700px;margin:0 auto;background:#fff;border-radius:16px;padding:40px;box-shadow:0 4px 6px rgba(0,0,0,0.1)}
h1{color:#6366f1;text-align:center;margin-bottom:10px;font-size:28px}
.date{text-align:center;color:#64748b;margin-bottom:30px;font-size:14px}
.section{margin-bottom:30px}
.section-title{color:#1f2937;font-size:18px;font-weight:bold;margin-bottom:15px;padding-bottom:8px;border-bottom:2px solid #e5e7eb}
.headline{background:linear-gradient(135deg,#fef3c7 0%,#fde68a 100%);padding:20px;border-radius:12px;border-left:4px solid #f59e0b;margin-bottom:20px}
.headline-title{color:#92400e;font-weight:bold;font-size:16px;margin-bottom:10px}
.headline-content{color:#78350f;line-height:1.6;font-size:14px}
.summary-box{background:#f3f4f6;padding:15px;border-radius:8px;margin-bottom:15px}
.summary-title{color:#374151;font-weight:600;margin-bottom:8px;font-size:14px}
.summary-content{color:#4b5563;line-height:1.6;font-size:13px}
.lang-label{display:inline-block;background:#6366f1;color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;margin-right:8px}
.link-box{background:linear-gradient(135deg,#6366f1 0%,#8b5cf6 100%);padding:20px;border-radius:12px;text-align:center;margin:30px 0}
.link-box a{color:#fff;font-size:16px;text-decoration:none;font-weight:bold}
.footer{margin-top:30px;padding-top:20px;border-top:1px solid #e5e7eb;color:#6b7280;font-size:12px;text-align:center}
</style>
</head>
<body>
<div class="container">
<h1>🤖 AI日报 v1.3</h1>
<div class="date">2026年3月3日 · Tuesday, March 3, 2026</div>

<div class="section">
<div class="section-title">🔥 今日头条 / Headlines</div>
<div class="headline">
<div class="headline-title">OpenAI完成1100亿美元史诗级融资，AI军备竞赛进入白热化阶段</div>
<div class="headline-content">OpenAI于3月2日宣布完成史上最大规模融资，金额高达1100亿美元，投后估值飙升至7300亿美元。本轮融资由Amazon领投500亿美元，NVIDIA投资300亿美元，软银投资300亿美元。</div>
</div>
<div class="summary-box">
<div class="summary-title"><span class="lang-label">EN</span>Headline Summary</div>
<div class="summary-content">OpenAI announced the largest private funding round in history on March 2, raising $110 billion with post-money valuation soaring to $730 billion. Led by Amazon ($5B), NVIDIA ($3B), and SoftBank ($3B).</div>
</div>
</div>

<div class="section">
<div class="section-title">🇨🇳 国内AI热点 / Domestic AI News</div>
<div class="summary-box">
<div class="summary-content">
• 银河通用再融25亿元，成估值最高未上市机器人公司<br>
• 松延动力完成近10亿元B轮融资，宁德时代系领投<br>
• 豆包大模型1.6发布：支持深度思考与256k长上下文<br>
• 可灵Kling 3.0发布：原生4K视频生成<br>
• 华为发布昇腾芯片路线图<br>
• 千寻智能连续完成两轮融资近20亿元
</div>
</div>
<div class="summary-box">
<div class="summary-title"><span class="lang-label">EN</span>Summary</div>
<div class="summary-content">
• Galbot Raises $362M, becomes highest-valued private robotics company<br>
• Songyan Power completes nearly $1B Series B, led by CATL<br>
• Doubao LLM 1.6 released with deep thinking and 256k context<br>
• Kling 3.0 released with native 4K video generation<br>
• Huawei unveils Ascend chip roadmap<br>
• Qianxun AI completes two consecutive rounds near $3B
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
• Amazon领投OpenAI 500亿美元
</div>
</div>
<div class="summary-box">
<div class="summary-title"><span class="lang-label">EN</span>Summary</div>
<div class="summary-content">
• AI Godfather Hinton warns: AI will replace more jobs in 2026<br>
• Google AI medical diagnosis system receives FDA breakthrough designation<br>
• GitHub Copilot X officially released<br>
• Claude 5 technical preview released with 90%+ SWE-bench score<br>
• Tesla FSD V15 begins rollout<br>
• Amazon leads OpenAI $50B investment
</div>
</div>
</div>

<div class="section">
<div class="section-title">🛍️ 零售AI应用实践 / Retail AI Practices</div>
<div class="summary-box">
<div class="summary-content">
• 阿里智能客服双11处理90%咨询，通义千问助力零售效率革命<br>
• Amazon Go "Just Walk Out"技术扩展至全食超市<br>
• Starbucks Deep Brew AI平台驱动个性化营销，销售额增长15%
</div>
</div>
<div class="summary-box">
<div class="summary-title"><span class="lang-label">EN</span>Summary</div>
<div class="summary-content">
• Alibaba smart customer service handled 90% of inquiries on Double 11<br>
• Amazon Go "Just Walk Out" technology expands to Whole Foods<br>
• Starbucks Deep Brew AI platform drives personalized marketing, sales grow 15%
</div>
</div>
</div>

<div class="link-box">
<a href="https://6085deaf.ai-daily-report-v1-3.pages.dev" target="_blank">📱 点击查看完整报告 / View Full Report →</a>
</div>

<div class="footer">
AI日报 v1.3 | Global AI Insights<br>
多语言支持：中文 · English · Français
</div>
</div>
</body>
</html>
'''

msg.attach(MIMEText(html, 'html', 'utf-8'))

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login('lunchwu@gmail.com', 'bize wlmw kupz jnoc')
server.sendmail('lunchwu@gmail.com', ['lunchwu@gmail.com'], msg.as_string())
server.quit()
print('✅ v1.3正式邮件已发送')