#!/bin/bash
# Cloudflare Pages 部署脚本
# 使用 Direct Upload API v2

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

# 计算文件哈希和大小
FILE_HASH=$(sha256sum index.html | awk '{print $1}')
FILE_SIZE=$(stat -c%s index.html)

echo "📊 文件大小: $FILE_SIZE bytes"
echo "🔐 文件哈希: $FILE_HASH"

# 步骤1: 创建部署会话（使用表单数据格式）
echo "📡 创建部署会话..."

# 创建 manifest JSON
MANIFEST=$(cat <<EOF
{"index.html":{"hash":"$FILE_HASH","size":"$FILE_SIZE"}}
EOF
)

echo "Manifest: $MANIFEST"

# 使用 multipart/form-data 格式
BOUNDARY="----FormBoundary7MA4YWxkTrZu0gW"

# 创建请求体
{
echo "------FormBoundary7MA4YWxkTrZu0gW"
echo 'Content-Disposition: form-data; name="manifest"'
echo ""
echo "$MANIFEST"
echo "------FormBoundary7MA4YWxkTrZu0gW"
echo 'Content-Disposition: form-data; name="branch"'
echo ""
echo "main"
echo "------FormBoundary7MA4YWxkTrZu0gW--"
} > /tmp/deploy_body.txt

RESPONSE=$(curl -s -X POST \
  "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/pages/projects/${PROJECT_NAME}/deployments" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: multipart/form-data; boundary=----FormBoundary7MA4YWxkTrZu0gW" \
  --data-binary @/tmp/deploy_body.txt)

echo "响应: $RESPONSE"

# 检查是否成功
if echo "$RESPONSE" | grep -q '"success":true'; then
    echo "✅ 部署会话创建成功!"
    
    # 提取上传 URL
    UPLOAD_URL=$(echo "$RESPONSE" | grep -o '"upload_url":"[^"]*"' | cut -d'"' -f4 | sed 's/\\u0026/\&/g')
    DEPLOYMENT_ID=$(echo "$RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
    
    if [ -n "$UPLOAD_URL" ]; then
        echo "📤 上传文件到: ${UPLOAD_URL:0:50}..."
        
        # 上传文件
        curl -s -X PUT "$UPLOAD_URL" \
          -H "Content-Type: application/octet-stream" \
          --data-binary @index.html
        
        echo "✅ 文件上传完成!"
    fi
    
    echo ""
    echo "🌐 部署成功!"
    echo "🔗 访问链接: https://${PROJECT_NAME}-32b.pages.dev"
    echo "📋 Deployment ID: $DEPLOYMENT_ID"
    
    # 清理
    rm -rf "$TMP_DIR" /tmp/deploy_body.txt
    
    exit 0
else
    echo "❌ 部署失败"
    echo "错误: $RESPONSE"
    
    # 清理
    rm -rf "$TMP_DIR" /tmp/deploy_body.txt
    
    exit 1
fi
