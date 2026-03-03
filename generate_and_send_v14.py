#!/usr/bin/env python3
"""
AI日报 v1.4 - 完整生成和发送脚本
6:30执行，7:00推送
"""

import subprocess
import sys
import time
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
    sys.stdout.flush()

def main():
    log("=== AI日报 v1.4 开始执行 ===")
    
    # 1. 拉取最新代码
    log("1. 拉取GitHub最新代码...")
    result = subprocess.run(['git', 'pull', 'origin', 'main'], 
                          cwd='/root/.openclaw/workspace',
                          capture_output=True, text=True)
    if result.returncode != 0:
        log(f"⚠️ Git pull失败: {result.stderr}")
    else:
        log("✅ Git pull成功")
    
    # 2. 等待到7:00
    now = datetime.now()
    target = now.replace(hour=7, minute=0, second=0, microsecond=0)
    if now > target:
        target = target.replace(day=target.day+1)
    
    wait_seconds = (target - now).total_seconds()
    if wait_seconds > 0:
        log(f"2. 等待到7:00推送，还需等待{wait_seconds/60:.1f}分钟...")
        time.sleep(wait_seconds)
    
    # 3. 发送日报
    log("3. 开始发送日报...")
    for i in range(5):
        try:
            result = subprocess.run(['python3', 'send_v13_daily.py'],
                                  cwd='/root/.openclaw/workspace',
                                  capture_output=True, text=True,
                                  timeout=120)
            if result.returncode == 0:
                log("✅ 日报发送成功")
                break
            else:
                log(f"⚠️ 发送失败({i+1}/5): {result.stderr}")
                time.sleep(3)
        except Exception as e:
            log(f"⚠️ 异常({i+1}/5): {e}")
            time.sleep(3)
    else:
        log("❌ 发送失败，将在7:05自动重试")
        return 1
    
    log("=== 执行完成 ===")
    return 0

if __name__ == '__main__':
    sys.exit(main())
