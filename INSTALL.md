# 阿星微信记账助手安装指南 / Axing WeChat Accounting Installation Guide

[English](#english-installation) | [中文](#中文安装)

---

## 中文安装

### 一键安装 / One-Click Install

在 OpenClaw 中执行：

```bash
openclaw skills install axing-wechat-accounting
```

或者手动安装：

```bash
cd ~/.openclaw/skills
git clone https://github.com/seeyouintokyo/axing-wechat-accounting.git
```

### 使用方法 / Usage

安装后，对 OpenClaw 说：

```
我想搭建微信记账助手
```

或

```
帮我配置微信记账
```

OpenClaw 会自动：
1. 检查并安装微信插件
2. 配置微信扫码登录
3. 创建飞书多维表格
4. 配置自动记账逻辑
5. （可选）配置月末报表和预算提醒

### 手动执行步骤 / Manual Steps

如果不想使用 Skill，也可以手动执行：

#### 1. 安装微信插件

```bash
openclaw plugins install "@tencent-weixin/openclaw-weixin@latest"
```

#### 2. 扫码登录

```bash
openclaw channels login --channel openclaw-weixin
```

按提示扫码完成登录。

#### 3. 重启 Gateway

```bash
openclaw gateway restart
```

#### 4. 创建多维表格

在飞书中创建「微信记账助手」多维表格，字段：
- 日期（日期）
- 类型（单选：支出/收入）
- 金额（数字）
- 分类（单选：餐饮/交通/购物/娱乐/通讯/居住/医疗/其他）
- 备注（文本）
- 来源（文本）

#### 5. 测试

在微信里发："午餐 35"

### 记账示例 / Examples

| 消息 | 识别结果 |
|------|---------|
| 午餐 35 | 支出 35元 餐饮 |
| 打车 20 | 支出 20元 交通 |
| 收入 5000 工资 | 收入 5000元 其他 |
| 火锅人均八十多 | 支出 80元 餐饮 |
| 鼠标98，椰子水10块 | 支出 98元 购物 + 支出 10元 餐饮 |

### 文件结构 / File Structure

```
axing-wechat-accounting/
├── SKILL.md              # 技能主文档 / Skill main doc
├── README.md             # 项目说明 / Project readme
├── INSTALL.md            # 安装说明 / Installation guide
├── scripts/
│   ├── setup.sh          # 一键安装脚本 / Setup script
│   ├── parse_accounting.py  # 消息解析 / Message parser
│   ├── monthly_report.py    # 月末报表 / Monthly report
│   └── budget_check.py      # 预算检查 / Budget check
└── references/           # 参考文档 / References
```

### 依赖 / Dependencies

- OpenClaw >= 2026.3.22
- 飞书应用权限：bitable:app, base:app:create
- 微信版本 >= 8.0.70

### 许可证 / License

MIT

---

## English Installation

### One-Click Install

Execute in OpenClaw:

```bash
openclaw skills install axing-wechat-accounting
```

Or install manually:

```bash
cd ~/.openclaw/skills
git clone https://github.com/seeyouintokyo/axing-wechat-accounting.git
```

### Usage

After installation, tell OpenClaw:

```
I want to set up a WeChat accounting assistant
```

Or

```
Help me configure WeChat accounting
```

OpenClaw will automatically:
1. Check and install WeChat plugin
2. Configure WeChat QR code login
3. Create Feishu Bitable
4. Configure auto-accounting logic
5. (Optional) Configure monthly report and budget alerts

### Manual Steps

If you don't want to use Skill, you can also execute manually:

#### 1. Install WeChat Plugin

```bash
openclaw plugins install "@tencent-weixin/openclaw-weixin@latest"
```

#### 2. Scan QR Code to Login

```bash
openclaw channels login --channel openclaw-weixin
```

Follow prompts to scan QR code and complete login.

#### 3. Restart Gateway

```bash
openclaw gateway restart
```

#### 4. Create Bitable

Create "WeChat Accounting" Bitable in Feishu with fields:
- Date (Date)
- Type (Single select: Expense/Income)
- Amount (Number)
- Category (Single select: Dining/Transport/Shopping/Entertainment/Communication/Housing/Medical/Other)
- Note (Text)
- Source (Text)

#### 5. Test

Send in WeChat: "Lunch 35"

### Examples

| Message | Recognized as |
|------|---------|
| Lunch 35 | Expense 35 CNY Dining |
| Taxi 20 | Expense 20 CNY Transport |
| Income 5000 salary | Income 5000 CNY Other |
| Hot pot average eighty | Expense 80 CNY Dining |
| Mouse 98, coconut water 10 | Expense 98 CNY Shopping + Expense 10 CNY Dining |

### File Structure

```
axing-wechat-accounting/
├── SKILL.md              # Skill main documentation
├── README.md             # Project readme
├── INSTALL.md            # Installation guide
├── scripts/
│   ├── setup.sh          # One-click setup script
│   ├── parse_accounting.py  # Message parser
│   ├── monthly_report.py    # Monthly report generator
│   └── budget_check.py      # Budget checker
└── references/           # Reference documents
```

### Dependencies

- OpenClaw >= 2026.3.22
- Feishu permissions: bitable:app, base:app:create
- WeChat version >= 8.0.70

### License

MIT
