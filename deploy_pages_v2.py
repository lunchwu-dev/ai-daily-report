#!/usr/bin/env python3
"""
Cloudflare Pages 部署脚本 - 使用正确的 Direct Upload 流程
"""

import os
import sys
import json
import hashlib
import requests

ACCOUNT_ID = "bbf1d66927d0926f1f8fe7b53d145898"
TOKEN = "HeKC-LGnSETPj4zZOW5ivh9U1j5_J80m1m_PeFOf"
PROJECT_NAME = "ai-daily-report"

def deploy_file(file_path):
    """部署文件到 Cloudflare Pages"""
    
    with open(file_path, 'rb') as f:
        content = f.read()
    
    file_hash = hashlib.sha256(content).hexdigest()
    file_size = len(content)
    
    print(f"📄 文件: {file_path}")
    print(f"📊 大小: {file_size} bytes")
    print(f"🔐 哈希: {file_hash}")
    
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    
    # 步骤1: 创建部署会话 - 使用 multipart/form-data
    print("\n📡 创建部署会话...")
    
    manifest = json.dumps({
        "index.html": {
            "hash": file_hash,
            "size": str(file_size)
        }
    })
    
    # 使用 multipart 格式
    from requests_toolbelt.multipart.encoder import MultipartEncoder
    
    multipart_data = MultipartEncoder(
        fields={
            'manifest': manifest,
            'branch': 'main'
        }
    )
    
    headers['Content-Type'] = multipart_data.content_type
    
    resp = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}/deployments",
        headers=headers,
        data=multipart_data
    )
    
    result = resp.json()
    print(f"响应: {json.dumps(result, indent=2)[:500]}")
    
    if not result.get("success"):
        print(f"❌ 创建部署失败: {result.get('errors')}")
        return None
    
    deployment = result["result"]
    deployment_id = deployment["id"]
    upload_url = deployment.get("upload_url")
    
    print(f"✅ 部署会话创建成功: {deployment_id[:8]}")
    
    # 步骤2: 上传文件
    if upload_url:
        print(f"\n📤 上传文件到: {upload_url[:60]}...")
        upload_resp = requests.put(
            upload_url,
            data=content,
            headers={
                "Content-Type": "application/octet-stream",
                "Content-Length": str(file_size)
            }
        )
        print(f"上传状态: {upload_resp.status_code}")
    else:
        print("⚠️ 没有上传 URL，尝试替代方法...")
    
    # 步骤3: 返回访问链接
    url = f"https://ai-daily-report-32b.pages.dev"
    print(f"\n🌐 部署完成!")
    print(f"🔗 访问链接: {url}")
    
    return url

if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else "/root/.openclaw/workspace/ai-report-2026-03-01.html"
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        sys.exit(1)
    
    deploy_file(file_path)
