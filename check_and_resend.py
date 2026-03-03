#!/usr/bin/env python3
"""
AI日报 v1.4 - 7:05推送检测和重试脚本
"""

import subprocess
import sys
import time
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
    sys.stdout.flush()

def main():
    log("=== 推送检测和重试 ===")
    
    # 检查今天是否已发送
    # 简化：直接重试发送
    for i in range(10):
        try:
            log(f"尝试发送({i+1}/10)...")
            result = subprocess.run(['python3', 'send_v13_daily.py'],
                                  cwd='/root/.openclaw/workspace',
                                  capture_output=True, text=True,
                                  timeout=120)
            if result.returncode == 0:
                log("✅ 日报发送成功")
                return 0
            else:
                log(f"⚠️ 失败: {result.stderr[:100]}")
                time.sleep(10)
        except Exception as e:
            log(f"⚠️ 异常: {e}")
            time.sleep(10)
    
    log("❌ 多次重试后仍失败，请手动检查")
    return 1

if __name__ == '__main__':
    sys.exit(main())
