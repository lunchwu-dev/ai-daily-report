#!/usr/bin/env python3
"""
发送邮件报告 - 读取JSON双语摘要文件
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

# 主收件人
RECIPIENT_EMAIL = "lunchwu@gmail.com"

# 抄送列表（暂时为空）
CC_EMAILS = []

def load_summary_from_json(file_path):
    """从JSON文件加载双语摘要"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        date = data.get('date', datetime.now().strftime("%Y年%m月%d日"))
        top3 = data.get('top3', [])
        
        # 构建中文摘要
        summary_cn = ""
        for item in top3[:3]:
            summary_cn += f"<p><strong>{item['rank']}. {item['title_cn']}</strong><br/>{item['summary_cn']}</p>"
        
        # 构建英文摘要
        summary_en = ""
        for item in top3[:3]:
            summary_en += f"<p><strong>{item['rank']}. {item['title_en']}</strong><br/>{item['summary_en']}</p>"
        
        return date, summary_cn, summary_en, len(top3)
        
    except Exception as e:
        print(f"⚠️ 读取JSON摘要失败: {e}")
        # 返回默认内容
        return (
            datetime.now().strftime("%Y年%m月%d日"),
            "<p>报告已生成，请查看完整内容</p>",
            "<p>Report generated. Please view full report.</p>",
            0
        )

def send_daily_report(report_file, cc_list=None):
    """发送每日AI报告邮件"""
    
    print(f"📄 正在处理报告: {report_file}")
    
    # 从文件路径推断JSON摘要文件路径
    json_file = report_file.replace('.html', '-summary.json')
    
    # 加载双语摘要
    report_date, summary_cn, summary_en, event_count = load_summary_from_json(json_file)
    
    print(f"📅 报告日期: {report_date}")
    print(f"📊 提取到 {event_count} 条热点")
    
    # 检查摘要是否有效
    if event_count < 3:
        print("❌ 热点事件数量不足，取消发送")
        return False
    
    # 构建报告URL - 使用主项目域名
    report_url = "https://a620c5bf.ai-daily-report-32b.pages.dev"
    
    subject = f"📰 AI Daily Report | {report_date}"
    
    body = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        h2 {{ color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
        h3 {{ color: #333; margin-top: 25px; }}
        h4 {{ color: #667eea; margin: 15px 0 10px; font-size: 1rem; }}
        .link-box {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 15px; border-radius: 10px; margin: 20px 0; text-align: center; }}
        .link-box a {{ color: white; text-decoration: none; font-weight: bold; font-size: 1.1rem; }}
        .summary {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #667eea; }}
        .summary p {{ margin: 8px 0; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 0.9rem; text-align: center; }}
    </style>
</head>
<body>
    <h2>📰 AI Daily Report | {report_date}</h2>
    
    <div class="link-box">
        <a href="{report_url}">📎 点击阅读完整报告</a>
    </div>
    
    <h3>📝 中文摘要</h3>
    <div class="summary">
        {summary_cn}
    </div>
    
    <h3>📝 English Summary</h3>
    <div class="summary">
        {summary_en}
    </div>
    
    <div class="footer">
        <p>此邮件由 AI 助手自动生成</p>
        <p>报告时间：{report_date} 07:30 (Asia/Shanghai)</p>
        <p><a href="https://ai-daily-report-index.pages.dev">查看历史报告 →</a></p>
    </div>
</body>
</html>"""
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    
    # 添加抄送
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
        return True
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # 从命令行参数获取报告文件路径
    if len(sys.argv) > 1:
        report_file = sys.argv[1]
    else:
        today = datetime.now().strftime("%Y-%m-%d")
        report_file = f"/root/.openclaw/workspace/ai-report-{today}.html"
    
    send_daily_report(report_file, cc_list=CC_EMAILS)
