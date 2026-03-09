<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Skill-ff6b35?style=for-the-badge" alt="OpenClaw Skill">
  <img src="https://img.shields.io/badge/模块-12个-blue?style=for-the-badge" alt="12 Modules">
  <img src="https://img.shields.io/badge/渠道-Discord%20%7C%20Telegram%20%7C%20Slack-5865F2?style=for-the-badge" alt="Channels">
  <img src="https://img.shields.io/badge/开源协议-MIT-green?style=for-the-badge" alt="MIT License">
</p>

<h1 align="center">Community Manager</h1>

<p align="center">
  <strong>基于 <a href="https://github.com/openclaw/openclaw">OpenClaw</a> 的 AI 社群管理技能</strong>
</p>

<p align="center">
  自动化 FAQ 回复、每日摘要、新人引导、内容审核、情绪分析等功能 — 跨 Discord、Telegram 和 Slack 渠道。
</p>

<p align="center">
  <a href="#功能列表">功能列表</a> &bull;
  <a href="#快速开始">快速开始</a> &bull;
  <a href="#模块详情">模块详情</a> &bull;
  <a href="#配置说明">配置说明</a> &bull;
  <a href="./README.md">English</a>
</p>

---

## 功能列表

| 模块 | 描述 |
|------|------|
| **FAQ 自动回复** | 语义匹配知识库，自动回答重复问题 |
| **每日摘要** | 汇总热门话题、未回答问题和活跃度统计 |
| **新人引导** | 自动欢迎新成员，推送规则和资源 |
| **多语言支持** | 检测语言并用提问者的语言回复 |
| **内容审核** | 三级严重度体系（监控 / 警告 / 删除） |
| **情绪分析** | 滚动情绪追踪，负面情绪激增时预警管理员 |
| **知识沉淀** | 自动提取高质量问答对，归档到知识库 |
| **活跃度激励** | 每周排行榜、贡献追踪、角色奖励 |
| **智能路由** | 分类问题并建议正确的频道 |
| **事件检测** | 检测 raid 攻击、垃圾消息浪潮、大规模退群、链接洪水 |
| **定时公告** | 基于 Cron 的跨渠道定时公告 |
| **线索追踪** | 监控未回答的问题，超时自动提醒 |

## 快速开始

### 1. 安装 Skill

将文件夹复制到 OpenClaw 的 skills 目录：

```bash
cp -r community-manager/ ~/.openclaw/skills/community-manager/
```

或通过 OpenClaw CLI 安装：

```bash
openclaw skill install ./community-manager
```

### 2. 配置

创建 `~/.openclaw/community/config.json`：

```json
{
  "community_name": "我的社群",
  "primary_language": "zh",
  "channels": {
    "discord": {
      "guild_id": "你的服务器ID",
      "faq_channel": "频道ID",
      "digest_channel": "频道ID",
      "admin_channel": "频道ID"
    }
  },
  "features": {
    "faq": true,
    "digest": true,
    "onboarding": true,
    "moderation": true
  }
}
```

### 3. 使用

直接和你的 OpenClaw 助手对话：

- *"总结一下今天的聊天"*
- *"设置 FAQ 自动回复"*
- *"看看社群排行榜"*
- *"#support 里有没有没回答的问题？"*

## 模块详情

### 核心模块

- **FAQ 自动回复** — 语义匹配，可配置置信度阈值，支持多语言 FAQ 条目。详见 [`references/faq-guide.md`](references/faq-guide.md)。

- **每日摘要** — 生成结构化摘要：热门话题、未回答问题、活跃度统计。使用 [`scripts/digest.py`](scripts/digest.py)。详见 [`references/daily-digest.md`](references/daily-digest.md)。

- **新人引导** — 可自定义欢迎消息，内置防 raid 批量模式（10+ 人同时加入时触发单条批量欢迎）。

- **多语言支持** — 基于 LLM 的语言检测。用提问者的语言回复。短消息（< 5 词）跳过检测以避免误判。

- **内容审核** — 三级严重度：低（仅记录）、中（警告）、高（删除+警告）。永不自动封禁。详见 [`references/moderation-policies.md`](references/moderation-policies.md)。

### 高级模块

- **情绪分析** — 按频道滚动计算情绪分数（1小时/24小时/7天窗口）。情绪骤降时提醒管理员。详见 [`references/sentiment-tracking.md`](references/sentiment-tracking.md)。

- **知识沉淀** — 通过点赞、"谢谢"回复和管理员📌来检测高质量回答。自动提交待审核。详见 [`references/knowledge-extraction.md`](references/knowledge-extraction.md)。

- **活跃度激励** — 追踪回答问题、分享资源、帮助新人等贡献。每周排行榜 + "进步之星"轮换。

- **智能路由** — 按主题分类问题，建议正确频道。基于确认机制，不会强制移动消息。每人每小时最多 1 次建议。

- **事件检测** — 监控 raid、垃圾消息、大规模退群和链接洪水。可配置阈值。使用 [`scripts/event_detector.py`](scripts/event_detector.py)。

- **定时公告** — 支持 Cron 语法的定时消息，跨渠道同步发送，可启用/禁用而无需删除。

- **线索追踪** — 追踪问题并在超时后（默认 24 小时）提醒管理员。使用 [`scripts/thread_tracker.py`](scripts/thread_tracker.py)。

## 脚本工具

所有脚本均为独立的 Python 3 工具，无外部依赖：

| 脚本 | 用途 | 用法 |
|------|------|------|
| `digest.py` | 从消息生成每日摘要 | `python3 scripts/digest.py --input messages.json` |
| `event_detector.py` | 检测异常事件 | `python3 scripts/event_detector.py --input events.json` |
| `thread_tracker.py` | 追踪未回答的问题 | `python3 scripts/thread_tracker.py --input messages.json --timeout 24` |

## 配置说明

完整配置参考见 [`SKILL.md`](SKILL.md#configuration)。

主要配置项：

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `digest_time` | `"09:00"` | 每日摘要发送时间（UTC） |
| `moderation_level` | `"medium"` | 默认审核灵敏度 |
| `sentiment_alert_threshold` | `0.3` | 触发情绪预警的负面比例 |
| `thread_timeout_hours` | `24` | 问题标记为逾期的小时数 |
| `leaderboard_day` | `"monday"` | 每周排行榜发布日 |

## 项目结构

```
community-manager/
├── SKILL.md                              # Skill 定义（12 个模块）
├── references/
│   ├── faq-guide.md                      # FAQ 知识库配置指南
│   ├── daily-digest.md                   # 摘要工作流详情
│   ├── moderation-policies.md            # 审核严重度与升级策略
│   ├── sentiment-tracking.md             # 情绪评分方法论
│   └── knowledge-extraction.md           # 知识提取启发式规则
└── scripts/
    ├── digest.py                         # 消息摘要生成器
    ├── event_detector.py                 # 异常检测引擎
    └── thread_tracker.py                 # 未回答问题追踪器
```

## 参与贡献

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-module`)
3. 提交更改
4. Push 并创建 PR

## 开源协议

MIT License。详见 [LICENSE](LICENSE)。
