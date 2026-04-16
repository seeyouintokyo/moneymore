# 阿星微信记账助手 (Axing WeChat Accounting)

[English](#english) | [中文](#中文)

---

## 中文
[wechat：staraiwork]

一键搭建微信记账助手，实现微信消息自动记账到飞书多维表格。

### 功能特点

- ✅ **零代码配置**：全程自然语言交互，无需编程
- ✅ **自动安装**：自动检测并安装微信插件
- ✅ **智能识别**：AI 自动解析金额、分类、类型
- ✅ **多笔支持**：一句话记多笔（如"鼠标98，椰子水10块"）
- ✅ **中文数字**：支持中文数字（八十多、二十五块）
- ✅ **语音支持**：支持语音转文字记账
- ✅ **图片识别**：自动识别账单截图
- ✅ **月末报表**：自动生成月度收支统计
- ✅ **预算提醒**：超支或接近预算时自动提醒
- ✅ **即时反馈**：记账成功后立即回复确认

### 快速开始

#### 方式一：使用 Skill（推荐）

对 OpenClaw 说：
```
我想搭建微信记账助手
```

#### 方式二：手动安装

```bash
# 1. 安装微信插件
openclaw plugins install "@tencent-weixin/openclaw-weixin@latest"

# 2. 扫码登录
openclaw channels login --channel openclaw-weixin

# 3. 重启 Gateway
openclaw gateway restart
```

### 使用示例

在微信里发送：

| 消息 | 自动识别为 |
|------|-----------|
| 午餐 35 | 支出 35元 餐饮 |
| 打车 20 | 支出 20元 交通 |
| 收入 5000 工资 | 收入 5000元 其他 |
| 火锅人均八十多 | 支出 80元 餐饮 |
| 鼠标98，椰子水10块 | 支出 98元 购物 + 支出 10元 餐饮 |

### 技术架构

```
微信消息 → OpenClaw AI 解析 → 飞书多维表格
```

### 配置说明

#### 飞书多维表格字段

- **日期**：自动记录当天日期
- **类型**：单选（支出/收入）
- **金额**：数字类型
- **分类**：单选（餐饮/交通/购物/娱乐/通讯/居住/医疗/其他）
- **备注**：用户原始消息
- **来源**：微信用户ID

#### 自动分类规则

根据关键词自动匹配：
- 餐饮：吃饭、午餐、晚餐、奶茶、咖啡、火锅
- 交通：打车、地铁、公交、加油
- 购物：买东西、淘宝、京东、超市
- 娱乐：电影、游戏、KTV、旅游
- 通讯：话费、流量、宽带
- 居住：房租、水电、物业
- 医疗：医院、看病、药
- 其他：未匹配到的分类

### 依赖要求

- OpenClaw >= 2026.3.22
- 微信版本 >= 8.0.70
- 飞书应用权限：bitable:app, base:app:create

### 项目链接

- 飞书文档：[https://feishu.cn/docx/WWDedlFy5onNdGxCyfAcbqLEnFH](https://jcn0eqeifyvi.feishu.cn/base/WZt7b8OQUa8TewsYi6EceTrUnOe?table=tblkC3LjMcVJarzt&view=vewNwadPsB)
- GitHub：https://github.com/seeyouintokyo/axing-wechat-accounting

### 作者

阿星 (Axing)

### 许可证

MIT License

wechat：staraiwork

---

## English

One-click setup for WeChat accounting assistant, automatically record WeChat messages to Feishu Bitable.

### Features

- ✅ **Zero-code configuration**: Natural language interaction, no programming required
- ✅ **Auto-installation**: Automatically detect and install WeChat plugin
- ✅ **Smart recognition**: AI automatically parses amount, category, and type
- ✅ **Multi-record support**: Record multiple items in one message (e.g., "mouse 98, coconut water 10")
- ✅ **Chinese numbers**: Support Chinese numerals (e.g., "eighty", "twenty-five")
- ✅ **Voice support**: Support voice-to-text accounting
- ✅ **Image recognition**: Automatically recognize bill screenshots
- ✅ **Monthly report**: Auto-generate monthly income/expense statistics
- ✅ **Budget alerts**: Alert when over budget or approaching limit
- ✅ **Instant feedback**: Reply confirmation immediately after recording

### Quick Start

#### Option 1: Use Skill (Recommended)

Tell OpenClaw:
```
I want to set up a WeChat accounting assistant
```

#### Option 2: Manual Installation

```bash
# 1. Install WeChat plugin
openclaw plugins install "@tencent-weixin/openclaw-weixin@latest"

# 2. Scan QR code to login
openclaw channels login --channel openclaw-weixin

# 3. Restart Gateway
openclaw gateway restart
```

### Usage Examples

Send messages in WeChat:

| Message | Auto-recognized as |
|------|-----------|
| Lunch 35 | Expense 35 CNY Dining |
| Taxi 20 | Expense 20 CNY Transport |
| Income 5000 salary | Income 5000 CNY Other |
| Hot pot average eighty | Expense 80 CNY Dining |
| Mouse 98, coconut water 10 | Expense 98 CNY Shopping + Expense 10 CNY Dining |

### Technical Architecture

```
WeChat Message → OpenClaw AI Parsing → Feishu Bitable
```

### Configuration

#### Feishu Bitable Fields

- **Date**: Auto-record current date
- **Type**: Single select (Expense/Income)
- **Amount**: Number
- **Category**: Single select (Dining/Transport/Shopping/Entertainment/Communication/Housing/Medical/Other)
- **Note**: Original user message
- **Source**: WeChat user ID

#### Auto-categorization Rules

Match based on keywords:
- Dining: eat, lunch, dinner, milk tea, coffee, hot pot
- Transport: taxi, subway, bus, gas
- Shopping: buy, Taobao, JD, supermarket
- Entertainment: movie, game, KTV, travel
- Communication: phone bill, data, broadband
- Housing: rent, utilities, property
- Medical: hospital, doctor, medicine
- Other: Uncategorized

### Requirements

- OpenClaw >= 2026.3.22
- WeChat version >= 8.0.70
- Feishu permissions: bitable:app, base:app:create

### Links

- Feishu Doc: [https://feishu.cn/docx/WWDedlFy5onNdGxCyfAcbqLEnFH](https://jcn0eqeifyvi.feishu.cn/base/WZt7b8OQUa8TewsYi6EceTrUnOe?table=tblkC3LjMcVJarzt&view=vewNwadPsB)
- GitHub: https://github.com/seeyouintokyo/axing-wechat-accounting

### Author

Axing (阿星)

### License

MIT License
