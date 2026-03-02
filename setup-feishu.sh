#!/bin/bash
# 飞书机器人配置脚本

echo "=== 飞书机器人配置 ==="
echo ""
echo "请输入你的飞书应用信息："
echo ""

read -p "App ID (cli_xxxx): " APP_ID
read -p "App Secret: " APP_SECRET

echo ""
echo "正在配置..."

openclaw config set channels.feishu.appId "$APP_ID"
openclaw config set channels.feishu.appSecret "$APP_SECRET"
openclaw config set channels.feishu.enabled true
openclaw config set channels.feishu.connectionMode "websocket"
openclaw config set channels.feishu.dmPolicy "pairing"
openclaw config set channels.feishu.groupPolicy "allowlist"
openclaw config set channels.feishu.requireMention true

echo ""
echo "配置完成！"
echo ""
echo "现在需要重启 OpenClaw 网关来应用配置。"
read -p "是否立即重启? (y/n): " RESTART

if [ "$RESTART" = "y" ] || [ "$RESTART" = "Y" ]; then
    echo "正在重启网关..."
    openclaw gateway restart
else
    echo "请稍后手动运行: openclaw gateway restart"
fi
