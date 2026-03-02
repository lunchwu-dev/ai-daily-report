#!/usr/bin/env python3
"""
Cloudflare Pages 部署脚本 - 使用 Direct Upload
"""

import os
import sys
import json
import hashlib
import base64
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
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    # 步骤1: 创建部署会话
    print("\n📡 创建部署会话...")
    
    manifest = {
        "index.html": {
            "hash": file_hash,
            "size": str(file_size)
        }
    }
    
    deploy_data = {
        "branch": "main",
        "manifest": manifest
    }
    
    resp = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}/deployments",
        headers=headers,
        json=deploy_data
    )
    
    result = resp.json()
    
    if not result.get("success"):
        print(f"❌ 创建部署失败: {result.get('errors')}")
        return None
    
    deployment = result["result"]
    deployment_id = deployment["id"]
    upload_url = deployment.get("upload_url")
    
    print(f"✅ 部署会话创建成功: {deployment_id[:8]}")
    
    # 步骤2: 如果有上传 URL，上传文件
    if upload_url:
        print(f"\n📤 上传文件...")
        upload_resp = requests.put(
            upload_url,
            data=content,
            headers={
                "Content-Type": "application/octet-stream",
                "Content-Length": str(file_size)
            }
        )
        
        if upload_resp.status_code in [200, 201]:
            print("✅ 文件上传成功!")
        else:
            print(f"⚠️ 上传返回: {upload_resp.status_code}")
    
    # 步骤3: 等待部署完成
    print("\n⏳ 等待部署完成...")
    import time
    time.sleep(3)
    
    # 检查部署状态
    status_resp = requests.get(
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}/deployments/{deployment_id}",
        headers=headers
    )
    
    status_result = status_resp.json()
    if status_result.get("success"):
        stage = status_result["result"].get("latest_stage", {})
        print(f"📊 部署状态: {stage.get('name', 'unknown')} - {stage.get('status', 'unknown')}")
    
    # 返回访问链接
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
