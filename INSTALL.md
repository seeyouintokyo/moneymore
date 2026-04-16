# 微信记账助手 Skill 安装指南

## 一键安装

在 OpenClaw 中执行：

```bash
openclaw skills install wechat-accounting
```

或者手动安装：

```bash
cd ~/.openclaw/skills
git clone <repository-url> wechat-accounting
```

## 使用方法

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

## 手动执行步骤

如果不想使用 Skill，也可以手动执行：

### 1. 安装微信插件
```bash
openclaw plugins install "@tencent-weixin/openclaw-weixin@latest"
```

### 2. 扫码登录
```bash
openclaw channels login --channel openclaw-weixin
```
按提示扫码完成登录。

### 3. 重启 Gateway
```bash
openclaw gateway restart
```

### 4. 创建多维表格
在飞书中创建「微信记账助手」多维表格，字段：
- 日期（日期）
- 类型（单选：支出/收入）
- 金额（数字）
- 分类（单选：餐饮/交通/购物/娱乐/通讯/居住/医疗/其他）
- 备注（文本）
- 来源（文本）

### 5. 测试
在微信里发："午餐 35"

## 记账示例

| 消息 | 识别结果 |
|------|---------|
| 午餐 35 | 支出 35元 餐饮 |
| 打车 20 | 支出 20元 交通 |
| 收入 5000 工资 | 收入 5000元 其他 |
| 买奶茶 15 | 支出 15元 餐饮 |
| 交话费 100 | 支出 100元 通讯 |

## 文件结构

```
wechat-accounting/
├── SKILL.md              # 技能主文档
├── INSTALL.md            # 安装说明
├── scripts/
│   ├── setup.sh          # 一键安装脚本
│   └── parse_accounting.py  # 消息解析脚本
└── references/           # 参考文档
```

## 依赖

- OpenClaw >= 2026.3.22
- 飞书应用权限：bitable:app, base:app:create
- 微信版本 >= 8.0.70

## 许可证

MIT
