---
name: axing-wechat-accounting
description: |
  阿星微信记账助手 - 一键搭建微信自动记账系统。
  Axing WeChat Accounting - One-click setup for WeChat auto-accounting.
  
  支持功能 / Features:
  - 微信消息自动记账 / Auto-record from WeChat messages
  - 支持中文数字和阿拉伯数字 / Support Chinese and Arabic numerals
  - 支持多笔记录 / Support multiple records
  - 月末自动报表 / Monthly auto-report
  - 预算超支提醒 / Budget overrun alerts
  
  触发条件 / Triggers: "我想记账", "微信记账", "I want to track expenses", "accounting assistant"
---

# 阿星微信记账助手 / Axing WeChat Accounting

[English](#english-guide) | [中文指南](#中文指南)

---

## 中文指南

一键完成微信记账助手的全套搭建。

### 功能概述 / Features

1. **微信记账** - 发消息自动记录（支持多笔、中文数字）
2. **月末报表** - 每月自动生成收支统计并推送
3. **预算提醒** - 超支或接近预算时自动提醒

### 支持的金额格式 / Supported Amount Formats

- 阿拉伯数字："35"、"100.5"
- 中文数字："八十"、"二十五"、"一百多"
- 复杂表达："人均八十多"、"花了二十五块"
- 多笔记录："鼠标98，椰子水10块"

### 执行流程 / Setup Process

#### Step 1: 检查并安装微信插件

```bash
openclaw plugins list | grep -i weixin
```

如果没有安装：
```bash
openclaw plugins install "@tencent-weixin/openclaw-weixin@latest"
```

#### Step 2: 配置微信登录

```bash
openclaw channels login --channel openclaw-weixin
```

按提示扫码完成登录。

#### Step 3: 重启 Gateway

```bash
openclaw gateway restart
```

#### Step 4: 创建飞书多维表格

创建「微信记账助手」表格，字段：
- 日期（DateTime）
- 类型（SingleSelect：支出/收入）
- 金额（Number）
- 分类（SingleSelect：餐饮/交通/购物/娱乐/通讯/居住/医疗/其他）
- 备注（Text）
- 来源（Text）

#### Step 5: 配置自动记账

收到微信消息时：
1. 判断是否是记账消息
2. 调用 `scripts/parse_accounting.py` 解析
3. 写入飞书表格
4. 检查预算
5. 回复用户

#### Step 6: 配置月末报表（可选）

```bash
openclaw cron add --name "monthly-report" --schedule "0 9 1 * *" \
  --command "生成并推送上月报表"
```

#### Step 7: 配置预算提醒（可选）

设置每月预算，每次记账后检查累计支出。

---

## English Guide

One-click setup for complete WeChat accounting assistant.

### Features

1. **WeChat Accounting** - Auto-record from messages (multi-record, Chinese numerals supported)
2. **Monthly Report** - Auto-generate monthly statistics and push
3. **Budget Alerts** - Alert when over budget or approaching limit

### Supported Amount Formats

- Arabic numerals: "35", "100.5"
- Chinese numerals: "八十" (eighty), "二十五" (twenty-five), "一百多" (around 100)
- Complex expressions: "人均八十多" (average eighty), "花了二十五块" (spent twenty-five)
- Multi-records: "mouse 98, coconut water 10"

### Setup Process

#### Step 1: Check and Install WeChat Plugin

```bash
openclaw plugins list | grep -i weixin
```

If not installed:
```bash
openclaw plugins install "@tencent-weixin/openclaw-weixin@latest"
```

#### Step 2: Configure WeChat Login

```bash
openclaw channels login --channel openclaw-weixin
```

Scan QR code to complete login.

#### Step 3: Restart Gateway

```bash
openclaw gateway restart
```

#### Step 4: Create Feishu Bitable

Create "WeChat Accounting" table with fields:
- Date (DateTime)
- Type (SingleSelect: Expense/Income)
- Amount (Number)
- Category (SingleSelect: Dining/Transport/Shopping/Entertainment/Communication/Housing/Medical/Other)
- Note (Text)
- Source (Text)

#### Step 5: Configure Auto-Accounting

When receiving WeChat message:
1. Check if it's an accounting message
2. Call `scripts/parse_accounting.py` to parse
3. Write to Feishu table
4. Check budget
5. Reply to user

#### Step 6: Configure Monthly Report (Optional)

```bash
openclaw cron add --name "monthly-report" --schedule "0 9 1 * *" \
  --command "Generate and push last month's report"
```

#### Step 7: Configure Budget Alerts (Optional)

Set monthly budget, check cumulative expenses after each record.

---

## 技术细节 / Technical Details

### 金额识别 / Amount Recognition

```python
# 阿拉伯数字 / Arabic numerals
"35" → 35
"100.5" → 100.5

# 中文数字 / Chinese numerals
"八十" → 80
"二十五" → 25
"一百多" → 100

# 多笔 / Multi-records
"鼠标98，椰子水10块" → [98, 10]
```

### 分类映射 / Category Mapping

```python
CATEGORY_KEYWORDS = {
    "餐饮/Dining": ["吃饭/eat", "午餐/lunch", "晚餐/dinner", "火锅/hot pot"],
    "交通/Transport": ["打车/taxi", "地铁/subway", "公交/bus"],
    "购物/Shopping": ["买东西/buy", "淘宝/Taobao", "京东/JD"],
    "娱乐/Entertainment": ["电影/movie", "游戏/game", "KTV"],
    "通讯/Communication": ["话费/phone", "流量/data", "宽带/broadband"],
    "居住/Housing": ["房租/rent", "水电/utilities", "物业/property"],
    "医疗/Medical": ["医院/hospital", "看病/doctor", "药/medicine"],
}
```

### 依赖工具 / Required Tools

- `openclaw plugins install` - 安装插件 / Install plugin
- `openclaw channels login` - 渠道登录 / Channel login
- `openclaw gateway restart` - 重启 gateway / Restart gateway
- `openclaw cron` - 定时任务 / Scheduled tasks
- `feishu_bitable_create_app` - 创建表格 / Create table
- `feishu_bitable_create_record` - 写入记录 / Write record
- `feishu_bitable_list_records` - 查询记录 / Query records
- `scripts/parse_accounting.py` - 消息解析 / Message parsing
- `scripts/monthly_report.py` - 月末报表 / Monthly report
- `scripts/budget_check.py` - 预算检查 / Budget check
