# 阿星微信记账助手 (Axing WeChat Accounting)

[English](#english) | [中文](#中文)

---

## 中文
[wechat：staraiwork]

### 项目背景

这是一个 **OpenClaw Skill（技能）**，必须配合 OpenClaw 使用。通过 OpenClaw 接收微信消息，AI 自动解析后写入飞书多维表格，实现「说一句就记账」的零代码方案。

### 核心能力

- **双引擎解析**：规则引擎（快速）+ AI 兜底（智能），自动选择最优方案
- **中文数字**：支持「八十多」「二十五块」等中文表达
- **多笔记录**：一句话记多笔，如「鼠标98，椰子水10块」
- **智能分类**：自动匹配餐饮/交通/购物等8大分类
- **月末报表**：自动生成月度收支统计
- **预算提醒**：超支时自动预警

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

# 4. 创建飞书多维表格
# 字段：日期、类型（支出/收入）、金额、分类、备注、来源

# 5. （可选）配置 AI 兜底
# 编辑 scripts/ai_parse_accounting.py，接入 OpenAI/Claude/Kimi API
```

### 使用示例

在微信里发送：

| 消息 | 识别结果 |
|------|---------|
| 午餐 35 | 支出 35元 餐饮 |
| 打车 20 | 支出 20元 交通 |
| 收入 5000 工资 | 收入 5000元 其他 |
| 火锅人均八十多 | 支出 80元 餐饮 |
| 鼠标98，椰子水10块 | 支出 98元 购物 + 支出 10元 餐饮 |

### AI 兜底说明

**默认使用规则引擎**，无需配置 API 即可使用。

如需启用 AI 兜底（提升复杂表达识别率）：
1. 编辑 `scripts/ai_parse_accounting.py`
2. 在 `call_llm_parse()` 函数中接入你的 LLM API
3. 支持 OpenAI、Claude、Kimi 等任意模型

示例配置：
```python
def call_llm_parse(text):
    import openai
    openai.api_key = "your-api-key"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": text}]
    )
    return json.loads(response.choices[0].message.content)
```

### 技术架构

```
微信消息 → OpenClaw → 规则引擎 → 低置信度? → AI兜底 → 飞书表格
                ↓ 高置信度
            直接写入
```

### 依赖

- OpenClaw >= 2026.3.22
- 微信版本 >= 8.0.70
- 飞书应用权限：bitable:app, base:app:create
- （可选）LLM API Key

### 链接

<<<<<<< HEAD
- GitHub：https://github.com/seeyouintokyo/moneymore
- 飞书文档：https://feishu.cn/docx/WWDedlFy5onNdGxCyfAcbqLEnFH
=======
- 飞书文档：[https://feishu.cn/docx/WWDedlFy5onNdGxCyfAcbqLEnFH](https://jcn0eqeifyvi.feishu.cn/base/WZt7b8OQUa8TewsYi6EceTrUnOe?table=tblkC3LjMcVJarzt&view=vewNwadPsB)
- GitHub：https://github.com/seeyouintokyo/axing-wechat-accounting

### 作者

阿星 (Axing)
>>>>>>> a412b615fbe502f249c839c3db157f00687319e2

### 许可证

MIT License

wechat：staraiwork

---

## English

### Project Background

This is an **OpenClaw Skill** that works with OpenClaw. It receives WeChat messages through OpenClaw, AI parses them automatically, and writes to Feishu Bitable for zero-code accounting.

### Core Capabilities

- **Dual-engine parsing**: Rule engine (fast) + AI fallback (smart), auto-selects optimal solution
- **Chinese numerals**: Supports expressions like "eighty" and "twenty-five"
- **Multi-record**: Record multiple items in one sentence, e.g., "mouse 98, coconut water 10"
- **Smart categorization**: Auto-matches 8 categories (Dining/Transport/Shopping/etc.)
- **Monthly report**: Auto-generates monthly statistics
- **Budget alerts**: Alerts when over budget

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

# 4. Create Feishu Bitable
# Fields: Date, Type (Expense/Income), Amount, Category, Note, Source

# 5. (Optional) Configure AI fallback
# Edit scripts/ai_parse_accounting.py, connect your LLM API
```

### Usage Examples

Send messages in WeChat:

| Message | Recognized as |
|------|---------|
| Lunch 35 | Expense 35 CNY Dining |
| Taxi 20 | Expense 20 CNY Transport |
| Income 5000 salary | Income 5000 CNY Other |
| Hot pot average eighty | Expense 80 CNY Dining |
| Mouse 98, coconut water 10 | Expense 98 CNY Shopping + Expense 10 CNY Dining |

### AI Fallback

**Uses rule engine by default**, no API configuration needed.

To enable AI fallback (improves complex expression recognition):
1. Edit `scripts/ai_parse_accounting.py`
2. Connect your LLM API in `call_llm_parse()` function
3. Supports OpenAI, Claude, Kimi, etc.

Example configuration:
```python
def call_llm_parse(text):
    import openai
    openai.api_key = "your-api-key"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": text}]
    )
    return json.loads(response.choices[0].message.content)
```

### Architecture

```
WeChat → OpenClaw → Rule Engine → Low confidence? → AI Fallback → Feishu
              ↓ High confidence
          Direct write
```

### Dependencies

- OpenClaw >= 2026.3.22
- WeChat version >= 8.0.70
- Feishu permissions: bitable:app, base:app:create
- (Optional) LLM API Key

### Links

<<<<<<< HEAD
- GitHub: https://github.com/seeyouintokyo/moneymore
- Feishu Doc: https://feishu.cn/docx/WWDedlFy5onNdGxCyfAcbqLEnFH
=======
- Feishu Doc: [https://feishu.cn/docx/WWDedlFy5onNdGxCyfAcbqLEnFH](https://jcn0eqeifyvi.feishu.cn/base/WZt7b8OQUa8TewsYi6EceTrUnOe?table=tblkC3LjMcVJarzt&view=vewNwadPsB)
- GitHub: https://github.com/seeyouintokyo/axing-wechat-accounting

### Author

Axing (阿星)
>>>>>>> a412b615fbe502f249c839c3db157f00687319e2

### License

MIT License
