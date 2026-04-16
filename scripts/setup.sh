#!/bin/bash
# 微信记账助手 - 一键安装脚本

set -e

echo "🚀 开始搭建微信记账助手..."

# 1. 检查微信插件
echo "📦 检查微信插件..."
if openclaw plugins list 2>/dev/null | grep -q "openclaw-weixin"; then
    echo "✅ 微信插件已安装"
else
    echo "📥 安装微信插件..."
    openclaw plugins install "@tencent-weixin/openclaw-weixin@latest"
    echo "✅ 微信插件安装完成"
fi

# 2. 检查微信登录
echo "🔐 检查微信登录状态..."
if openclaw status 2>/dev/null | grep -q "openclaw-weixin.*OK"; then
    echo "✅ 微信已登录"
else
    echo "📱 请扫码登录微信..."
    openclaw channels login --channel openclaw-weixin
fi

# 3. 重启 Gateway
echo "🔄 重启 Gateway..."
openclaw gateway restart
echo "✅ Gateway 重启完成"

echo ""
echo "🎉 基础配置完成！"
echo "下一步：创建飞书多维表格并配置记账逻辑"
