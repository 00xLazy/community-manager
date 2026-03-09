<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Skill-ff6b35?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHRleHQgeT0iMjAiIGZvbnQtc2l6ZT0iMjAiPvCfppA8L3RleHQ+PC9zdmc+" alt="OpenClaw Skill">
  <img src="https://img.shields.io/badge/Modules-12-blue?style=for-the-badge" alt="12 Modules">
  <img src="https://img.shields.io/badge/Channels-Discord%20%7C%20Telegram%20%7C%20Slack-5865F2?style=for-the-badge" alt="Channels">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License">
</p>

<h1 align="center">Community Manager</h1>

<p align="center">
  <strong>AI-powered community management skill for <a href="https://github.com/openclaw/openclaw">OpenClaw</a></strong>
</p>

<p align="center">
  Automate FAQ replies, daily digests, onboarding, moderation, sentiment analysis, and more — across Discord, Telegram, and Slack.
</p>

<p align="center">
  <a href="#features">Features</a> &bull;
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#bot-permissions">Bot Permissions</a> &bull;
  <a href="#modules">Modules</a> &bull;
  <a href="#configuration">Configuration</a> &bull;
  <a href="./README_CN.md">中文文档</a>
</p>

---

## Features

| Module | Description |
|--------|-------------|
| **FAQ Auto-Reply** | Semantic matching against a knowledge base, auto-answer repeated questions |
| **Daily Digest** | Summarize hot topics, unanswered questions, and activity stats |
| **New Member Onboarding** | Welcome newcomers with rules, resources, and role assignment |
| **Multilingual Support** | Detect language and reply in the user's language |
| **Content Moderation** | Three-tier severity system (monitor / warn / remove) |
| **Sentiment Analysis** | Rolling mood tracking with admin alerts on negative shifts |
| **Knowledge Extraction** | Auto-capture high-quality Q&A pairs into the knowledge base |
| **Engagement Gamification** | Weekly leaderboards, contribution tracking, role rewards |
| **Smart Routing** | Classify questions and suggest the right channel |
| **Event Detection** | Detect raids, spam waves, mass leaves, link floods |
| **Scheduled Announcements** | Cron-based, cross-channel, recurring announcements |
| **Thread Tracker** | Monitor unanswered questions with configurable timeouts |
| **AI Conversation Starter** | Auto-generate discussion topics during quiet periods |
| **Mentor Matching** | Pair newcomers with experienced members by expertise |
| **Polls & Surveys** | Community polls with auto-summarized results and AI insights |
| **AMA Mode** | Structured Q&A sessions with question queuing and upvoting |
| **Community Challenges** | Daily challenges, weekly quests, and collaborative goals |
| **Member Profiles** | Auto-generated expertise profiles based on activity |
| **Community Health Dashboard** | Comprehensive metrics, trends, and actionable insights |
| **Multilingual Bridge** | Real-time translation bridge between language-specific channels |

## Quick Start

### 1. Install the Skill

Copy this folder into your OpenClaw skills directory:

```bash
cp -r community-manager/ ~/.openclaw/skills/community-manager/
```

Or install via OpenClaw CLI:

```bash
openclaw skill install ./community-manager
```

### 2. Configure

Create `~/.openclaw/community/config.json`:

```json
{
  "community_name": "My Community",
  "primary_language": "en",
  "channels": {
    "discord": {
      "guild_id": "YOUR_GUILD_ID",
      "faq_channel": "CHANNEL_ID",
      "digest_channel": "CHANNEL_ID",
      "admin_channel": "CHANNEL_ID"
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

### 3. Use It

Just talk to your OpenClaw assistant:

- *"Summarize today's chat"*
- *"Set up FAQ auto-reply"*
- *"Show the community leaderboard"*
- *"Any unanswered questions in #support?"*

## Bot Permissions

Your OpenClaw bot needs specific permissions in each platform for the skill to work. Here's a quick overview:

### Discord
- Create a bot in [Developer Portal](https://discord.com/developers/applications)
- Enable **Message Content Intent** (required)
- Invite with permissions: Read Messages, Send Messages, Manage Messages, Manage Roles, Read Message History

### Telegram
- Create a bot via [@BotFather](https://t.me/BotFather)
- **Critical**: Run `/setprivacy` → `Disabled` (otherwise the bot can't see group messages)
- Add the bot to your group and set as **Admin** with "Delete messages" permission

### Slack
- Create a [Slack App](https://api.slack.com/apps) with OAuth scopes: `channels:history`, `chat:write`, `reactions:read`, `users:read`
- `/invite @your-bot` to each channel

For the full setup guide with per-feature permission matrix and troubleshooting, see [`references/setup-guide.md`](references/setup-guide.md).

## Modules

### Core

- **FAQ Auto-Reply** — Semantic matching with configurable confidence thresholds. Supports multilingual FAQ entries. See [`references/faq-guide.md`](references/faq-guide.md).

- **Daily Digest** — Generates structured summaries with hot topics, unanswered questions, and activity stats. Uses [`scripts/digest.py`](scripts/digest.py). See [`references/daily-digest.md`](references/daily-digest.md).

- **New Member Onboarding** — Customizable welcome messages with anti-raid batch mode (10+ simultaneous joins triggers single batch welcome).

- **Multilingual Support** — LLM-based language detection. Replies in the user's language. Skips detection for short messages (< 5 words).

- **Content Moderation** — Three severity levels: Low (log only), Medium (warn), High (delete + warn). Never auto-bans. See [`references/moderation-policies.md`](references/moderation-policies.md).

### Advanced

- **Sentiment Analysis** — Rolling sentiment scores per channel (1h/24h/7d windows). Alerts admin when mood drops sharply. See [`references/sentiment-tracking.md`](references/sentiment-tracking.md).

- **Knowledge Extraction** — Detects high-quality answers via reactions, "thanks" replies, and admin pins. Auto-submits for review. See [`references/knowledge-extraction.md`](references/knowledge-extraction.md).

- **Engagement Gamification** — Tracks answers given, resources shared, newcomers helped. Weekly leaderboard with "Rising Star" rotation.

- **Smart Routing** — Classifies questions by topic and suggests the correct channel. Confirmation-based, never force-moves. Max 1 suggestion per user per hour.

- **Event Detection** — Monitors for raids, spam waves, mass leaves, and link floods. Configurable thresholds. Uses [`scripts/event_detector.py`](scripts/event_detector.py).

- **Scheduled Announcements** — Cron syntax for recurring messages. Cross-channel simultaneous posting. Enable/disable without deleting.

- **Thread Tracker** — Tracks questions and alerts admin after configurable timeout (default 24h). Uses [`scripts/thread_tracker.py`](scripts/thread_tracker.py).

### Social & Engagement

- **AI Conversation Starter** — Auto-generates discussion topics during quiet periods. Varies topic types and tracks engagement. See [`references/conversation-starters.md`](references/conversation-starters.md).

- **Mentor Matching** — Pairs newcomers with experienced members based on expertise overlap, availability, and helpfulness. Opt-in for mentors. See [`references/mentor-matching.md`](references/mentor-matching.md).

- **Polls & Surveys** — Reaction-based or multi-question polls with auto-summarized results and AI insights. Anonymous by default.

- **AMA Mode** — Structured Ask-Me-Anything sessions with question queuing, upvoting, and auto-generated summaries.

- **Community Challenges** — Daily challenges, weekly quests, and collaborative community goals with a point system and badges. See [`references/community-challenges.md`](references/community-challenges.md).

- **Member Profiles** — Auto-generated expertise profiles based on activity, showing badges, skill areas, and contribution stats.

- **Community Health Dashboard** — Weekly/monthly reports with health score, growth, engagement, sentiment trends, and actionable recommendations. Uses [`scripts/health_report.py`](scripts/health_report.py).

- **Multilingual Bridge** — Real-time translation bridge between language-specific channels. Shows original text alongside translation.

## Scripts

All scripts are standalone Python 3 tools with no external dependencies:

| Script | Purpose | Usage |
|--------|---------|-------|
| `digest.py` | Generate daily digest from messages | `python3 scripts/digest.py --input messages.json` |
| `event_detector.py` | Detect anomalous events | `python3 scripts/event_detector.py --input events.json` |
| `thread_tracker.py` | Track unanswered questions | `python3 scripts/thread_tracker.py --input messages.json --timeout 24` |
| `health_report.py` | Generate community health report | `python3 scripts/health_report.py --input activity.json` |

## Configuration

Full configuration reference in [`SKILL.md`](SKILL.md#configuration).

Key config options:

| Option | Default | Description |
|--------|---------|-------------|
| `digest_time` | `"09:00"` | When to post daily digest (UTC) |
| `moderation_level` | `"medium"` | Default moderation sensitivity |
| `sentiment_alert_threshold` | `0.3` | Negative sentiment ratio to trigger alert |
| `thread_timeout_hours` | `24` | Hours before a question is flagged as overdue |
| `leaderboard_day` | `"monday"` | Day to post weekly leaderboard |

## Project Structure

```
community-manager/
├── SKILL.md                              # Skill definition (20 modules)
├── references/
│   ├── setup-guide.md                    # Bot permissions & platform setup
│   ├── faq-guide.md                      # FAQ knowledge base configuration
│   ├── daily-digest.md                   # Digest workflow details
│   ├── moderation-policies.md            # Moderation severity & escalation
│   ├── sentiment-tracking.md             # Sentiment scoring methodology
│   ├── knowledge-extraction.md           # Knowledge capture heuristics
│   ├── conversation-starters.md          # Discussion topic templates
│   ├── mentor-matching.md                # Mentor matching algorithm
│   └── community-challenges.md           # Challenge & quest templates
└── scripts/
    ├── digest.py                         # Message digest generator
    ├── event_detector.py                 # Anomaly detection engine
    ├── thread_tracker.py                 # Unanswered question tracker
    └── health_report.py                  # Community health report generator
```

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-module`)
3. Commit your changes
4. Push and open a PR

## License

MIT License. See [LICENSE](LICENSE) for details.
