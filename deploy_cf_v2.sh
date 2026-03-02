#!/bin/bash
# Cloudflare Pages 部署脚本 - 修正版

ACCOUNT_ID="bbf1d66927d0926f1f8fe7b53d145898"
TOKEN="HeKC-LGnSETPj4zZOW5ivh9U1j5_J80m1m_PeFOf"
PROJECT_NAME="ai-daily-report"
FILE_PATH="${1:-/root/.openclaw/workspace/ai-report-2026-03-01.html}"

echo "🚀 开始部署到 Cloudflare Pages..."
echo "📄 文件: $FILE_PATH"

# 创建临时目录
TMP_DIR=$(mktemp -d)
cp "$FILE_PATH" "$TMP_DIR/index.html"
cd "$TMP_DIR"

# 计算文件哈希
FILE_HASH=$(sha256sum index.html | awk '{print $1}')
FILE_SIZE=$(stat -c%s index.html)

echo "📊 文件大小: $FILE_SIZE bytes"
echo "🔐 文件哈希: $FILE_HASH"

# 步骤1: 创建部署会话
echo "📡 创建部署会话..."

RESPONSE=$(curl -s -X POST \
  "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/pages/projects/${PROJECT_NAME}/deployments" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: multipart/form-data" \
  -F "manifest={\"index.html\":{\"hash\":\"$FILE_HASH\",\"size\":\"$FILE_SIZE\"}}" \
  -F "branch=main")

echo "响应: $(echo "$RESPONSE" | head -c 500)"

# 检查是否成功
if ! echo "$RESPONSE" | grep -q '"success":true'; then
    echo "❌ 创建部署会话失败"
    echo "错误: $RESPONSE"
    rm -rf "$TMP_DIR"
    exit 1
fi

echo "✅ 部署会话创建成功!"

# 提取关键信息
UPLOAD_URL=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['result'].get('upload_url',''))" 2>/dev/null)
DEPLOYMENT_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['result'].get('id',''))" 2>/dev/null)

echo "📋 Deployment ID: $DEPLOYMENT_ID"

# 步骤2: 上传文件
if [ -n "$UPLOAD_URL" ]; then
    echo "📤 上传文件..."
    
    UPLOAD_RESP=$(curl -s -X PUT "$UPLOAD_URL" \
      -H "Content-Type: application/octet-stream" \
      --data-binary @index.html)
    
    echo "上传响应: $UPLOAD_RESP"
fi

# 步骤3: 获取最终 URL
FINAL_URL="https://ai-daily-report-32b.pages.dev"

echo ""
echo "🌐 部署完成!"
echo "🔗 访问链接: $FINAL_URL"
echo "📋 部署ID: $DEPLOYMENT_ID"

# 清理
rm -rf "$TMP_DIR"

exit 0
