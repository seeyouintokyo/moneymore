# 微信记账助手 (WeChat Accounting)

一键搭建微信记账助手，实现微信消息自动记账到飞书多维表格。

## 功能特点

- ✅ **零代码配置**：全程自然语言交互，无需编程
- ✅ **自动安装**：自动检测并安装微信插件
- ✅ **智能识别**：AI 自动解析金额、分类、类型
- ✅ **语音支持**：支持语音转文字记账
- ✅ **即时反馈**：记账成功后立即回复确认

## 快速开始

### 方式一：使用 Skill（推荐）

对 OpenClaw 说：
```
我想搭建微信记账助手
```

### 方式二：手动安装

```bash
# 1. 安装微信插件
openclaw plugins install "@tencent-weixin/openclaw-weixin@latest"

# 2. 扫码登录
openclaw channels login --channel openclaw-weixin

# 3. 重启 Gateway
openclaw gateway restart
```

## 使用示例

在微信里发送：

| 消息 | 自动识别为 |
|------|-----------|
| 午餐 35 | 支出 35元 餐饮 |
| 打车 20 | 支出 20元 交通 |
| 收入 5000 工资 | 收入 5000元 其他 |
| 买奶茶 15 | 支出 15元 餐饮 |
| 交话费 100 | 支出 100元 通讯 |

## 技术架构

```
微信消息 → OpenClaw AI 解析 → 飞书多维表格
```

## 配置说明

### 飞书多维表格字段

- **日期**：自动记录当天日期
- **类型**：单选（支出/收入）
- **金额**：数字类型
- **分类**：单选（餐饮/交通/购物/娱乐/通讯/居住/医疗/其他）
- **备注**：用户原始消息
- **来源**：微信用户ID

### 自动分类规则

根据关键词自动匹配：
- 餐饮：吃饭、午餐、晚餐、奶茶、咖啡
- 交通：打车、地铁、公交、加油
- 购物：买东西、淘宝、京东、超市
- 娱乐：电影、游戏、KTV、旅游
- 通讯：话费、流量、宽带
- 居住：房租、水电、物业
- 医疗：医院、看病、药
- 其他：未匹配到的分类

## 依赖要求

- OpenClaw >= 2026.3.22
- 微信版本 >= 8.0.70
- 飞书应用权限：bitable:app, base:app:create

## 项目链接

- 飞书文档：https://feishu.cn/docx/WWDedlFy5onNdGxCyfAcbqLEnFH
- 多维表格示例：https://jcn0eqeifyvi.feishu.cn/base/ZK9wbXlUnaUl3yskGLrcnGM7nme

## 作者

OpenClaw Community

## 许可证

MIT License
