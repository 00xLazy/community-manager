<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Skill-ff6b35?style=for-the-badge" alt="OpenClaw Skill">
  <img src="https://img.shields.io/badge/模块-34个-blue?style=for-the-badge" alt="34 Modules">
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
  <a href="#bot-权限设置">Bot 权限设置</a> &bull;
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
| **AI 话题生成** | 冷场时自动生成讨论话题，保持社群活跃 |
| **导师匹配** | 根据专长自动为新人匹配经验丰富的导师 |
| **投票与调查** | 社群投票，自动汇总结果并生成 AI 洞察 |
| **AMA 模式** | 结构化问答环节，支持问题排队和投票优先 |
| **社群挑战** | 每日挑战、每周任务和协作式社群目标 |
| **成员档案** | 基于活动数据自动生成的专长档案 |
| **社群健康仪表盘** | 综合指标、趋势分析和可执行建议 |
| **多语言桥接** | 不同语言频道之间的实时翻译桥接 |
| **长讨论摘要** | 讨论超过阈值时自动生成 TL;DR |
| **今日回顾** | "历史上的今天"社群回忆帖 |
| **Office Hours** | 专家定期答疑，支持问题排队管理 |
| **协作项目板** | 社群协作项目组队、进度追踪、成果展示 |
| **流失预警** | 检测即将流失的活跃成员，触发挽留 |
| **成员关系图谱** | 可视化成员互动关系和社群结构 |
| **智能标签** | 按专长、行为模式自动给成员打标签 |
| **回流召回** | 个性化消息召回沉默成员 |
| **精华推荐** | 推荐相关的历史讨论和优质内容 |
| **社群 Wiki** | 从讨论中自动维护结构化知识库 |
| **内容创作激励** | 追踪和奖励原创教程、指南 |
| **反馈收集器** | 自动收集 Bug 报告、功能建议并分类汇总 |
| **社群日历** | 活动管理：创建、报名、提醒、活动回顾 |
| **管理员轮值** | 管理员自动排班和工作量追踪 |

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

## Bot 权限设置

你的 OpenClaw Bot 在各平台需要特定权限才能正常工作。以下是快速概览：

### Discord
- 在 [Developer Portal](https://discord.com/developers/applications) 创建 Bot
- 开启 **Message Content Intent**（必须）
- 邀请时勾选权限：读取消息、发送消息、管理消息、管理角色、读取消息历史

### Telegram
- 通过 [@BotFather](https://t.me/BotFather) 创建 Bot
- **关键步骤**：执行 `/setprivacy` → 选择 `Disabled`（否则 Bot 无法读取群内消息）
- 将 Bot 加入群组并设为**管理员**，开启"删除消息"权限

### Slack
- 创建 [Slack App](https://api.slack.com/apps)，配置 OAuth 权限：`channels:history`、`chat:write`、`reactions:read`、`users:read`
- 在每个频道执行 `/invite @your-bot`

完整的设置指南（含各功能权限矩阵和故障排除）见 [`references/setup-guide.md`](references/setup-guide.md)。

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

### 社交与互动模块

- **AI 话题生成** — 社群冷场时自动生成讨论话题，变换话题类型并追踪参与度。详见 [`references/conversation-starters.md`](references/conversation-starters.md)。

- **导师匹配** — 基于专长重合度、可用性和帮助力评分，为新人匹配导师。导师需主动开启。详见 [`references/mentor-matching.md`](references/mentor-matching.md)。

- **投票与调查** — 基于表情反应或按钮的投票，自动汇总结果并生成 AI 洞察。默认匿名。

- **AMA 模式** — 结构化问答环节，支持问题排队、投票优先、自动生成摘要。

- **社群挑战** — 每日挑战、每周任务和协作式社群目标，积分系统 + 徽章奖励。详见 [`references/community-challenges.md`](references/community-challenges.md)。

- **成员档案** — 基于活动数据自动生成专长档案，展示徽章、技能领域和贡献统计。

- **社群健康仪表盘** — 每周/月报告，包含健康评分、增长、活跃度、情绪趋势及可执行建议。使用 [`scripts/health_report.py`](scripts/health_report.py)。

- **多语言桥接** — 不同语言频道间的实时翻译桥接。翻译旁附原文，保持透明。

### 运营与分析模块

- **长讨论摘要** — 讨论超过可配置阈值（默认 50 条）时自动生成 TL;DR。随讨论增长自动更新。

- **今日回顾** — 每日"历史上的今天"帖子，展示热门讨论、社群里程碑和有趣时刻。详见 [`references/throwback-posts.md`](references/throwback-posts.md)。

- **Office Hours** — 定期专家答疑环节，支持问题预提交、排队管理、自动生成回顾摘要。

- **协作项目板** — 社群协作项目管理：发起项目、招募队友、追踪里程碑、展示成果。

- **社群日历** — 活动全生命周期管理：创建、报名、提醒（1周/1天/1小时）、活动后回顾。详见 [`references/community-calendar.md`](references/community-calendar.md)。

### 成员智能模块

- **流失预警** — 基于活跃度下降、负面互动、未回答问题等信号检测流失风险。仅管理员可见，附带建议操作。详见 [`references/churn-prediction.md`](references/churn-prediction.md)。

- **成员关系图谱** — 分析成员互动模式：社群簇、桥梁成员、孤立成员。月度洞察助力社群结构优化。

- **智能标签** — 自动为成员打上专长标签、角色标签和活跃标签。驱动智能路由、导师匹配和精准推送。

- **回流召回** — 基于成员历史和兴趣生成个性化召回消息，拉回沉默成员。详见 [`references/winback-campaigns.md`](references/winback-campaigns.md)。

- **精华推荐** — 推荐相关的历史讨论、指南和资源。每周"精华回顾"合集。

### 内容与知识模块

- **社群 Wiki** — 从 FAQ、讨论、答疑环节自动聚合维护结构化知识库。详见 [`references/community-wiki.md`](references/community-wiki.md)。

- **内容创作激励** — 追踪原创内容（教程、指南、代码分享），积分和徽章奖励创作者，月度创作者聚光灯。

- **反馈收集器** — 从自然对话中自动识别和分类 Bug 报告、功能建议和改进意见。去重后生成周报。

### 管理工具模块

- **管理员轮值** — 跨时区管理员自动排班。追踪工作量、检测空档、支持换班。

## 脚本工具

所有脚本均为独立的 Python 3 工具，无外部依赖：

| 脚本 | 用途 | 用法 |
|------|------|------|
| `digest.py` | 从消息生成每日摘要 | `python3 scripts/digest.py --input messages.json` |
| `event_detector.py` | 检测异常事件 | `python3 scripts/event_detector.py --input events.json` |
| `thread_tracker.py` | 追踪未回答的问题 | `python3 scripts/thread_tracker.py --input messages.json --timeout 24` |
| `health_report.py` | 生成社群健康报告 | `python3 scripts/health_report.py --input activity.json` |

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
| `thread_summary_threshold` | `50` | 触发长讨论自动摘要的消息数 |
| `churn_inactive_days` | `14` | 触发流失预警的不活跃天数 |
| `winback_cooldown_days` | `30` | 召回消息最小间隔天数 |
| `admin_shift_hours` | `8` | 管理员每班时长 |

## 项目结构

```
community-manager/
├── SKILL.md                              # Skill 定义（34 个模块）
├── references/
│   ├── setup-guide.md                    # Bot 权限与平台设置指南
│   ├── faq-guide.md                      # FAQ 知识库配置指南
│   ├── daily-digest.md                   # 摘要工作流详情
│   ├── moderation-policies.md            # 审核严重度与升级策略
│   ├── sentiment-tracking.md             # 情绪评分方法论
│   ├── knowledge-extraction.md           # 知识提取启发式规则
│   ├── conversation-starters.md          # 讨论话题模板
│   ├── mentor-matching.md                # 导师匹配算法
│   ├── community-challenges.md           # 挑战与任务模板
│   ├── throwback-posts.md               # 回顾帖内容选择规则
│   ├── churn-prediction.md              # 流失评分方法论
│   ├── winback-campaigns.md             # 召回消息模板
│   ├── community-wiki.md               # Wiki 组织架构
│   └── community-calendar.md           # 活动模板与报名追踪
└── scripts/
    ├── digest.py                         # 消息摘要生成器
    ├── event_detector.py                 # 异常检测引擎
    ├── thread_tracker.py                 # 未回答问题追踪器
    └── health_report.py                  # 社群健康报告生成器
```

## 参与贡献

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-module`)
3. 提交更改
4. Push 并创建 PR

## 开源协议

MIT License。详见 [LICENSE](LICENSE)。
