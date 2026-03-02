# AI日报生成系统

## 项目说明
自动生成全球AI大事件热点日报，包含中英文双语摘要。

## 文件说明

- `template.html` - HTML报告模板（响应式设计，支持PC/移动端）
- `send_email_report.py` - 邮件发送脚本
- `MEMORY.md` - 项目配置和凭证信息

## 报告结构
1. 国内热点事件（红色边框）
2. 海外热点事件（蓝色边框）
3. 业界领袖观点（紫色边框）
4. 市场情绪分析（绿色边框）
5. 明日关注预告（黄色边框）
6. 往期报告导航

## 样式特点
- 深色主题设计
- 响应式布局（PC端多栏，移动端单列）
- 每个热点事件包含真实来源链接
- 卡片式布局，圆角阴影效果

## 部署
- 主报告：Cloudflare Pages `ai-daily-report`
- 历史版本：`ai-daily-report-YYYY-MM-DD`
- 索引页面：`ai-daily-report-index`

## 定时任务
每天 7:30 AM (Asia/Shanghai) 自动生成并发送
