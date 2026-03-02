#!/bin/bash
set -e

export CLOUDFLARE_API_TOKEN="zObKBHBOkVJCVlICs4w7AYQyw-HWz3SWnys84fJB"

# 读取HTML和JSON内容
HTML_CONTENT=$(cat /root/.openclaw/workspace/ai-report-2026-03-02.html | sed 's/"/\\"/g' | tr '\n' ' ')
JSON_CONTENT=$(cat /root/.openclaw/workspace/ai-report-2026-03-02-summary.json | sed 's/"/\\"/g' | tr '\n' ' ')

# 创建主项目 Workers
echo "Deploying ai-daily-report..."
wrangler deploy --name ai-daily-report --compatibility-date 2026-03-02 index.js 2&1 || echo "Main deploy may need KV setup"

# 创建历史版本项目
echo "Deploying ai-daily-report-2026-03-02..."
wrangler deploy --name ai-daily-report-2026-03-02 --compatibility-date 2026-03-02 index.js 2&1 || echo "History deploy may need KV setup"

echo "Deployment commands executed"
