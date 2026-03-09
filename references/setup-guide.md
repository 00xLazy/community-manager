# Setup Guide — Bot Permissions by Platform

This guide covers how to set up your OpenClaw bot in each platform and the permissions required for each community-manager feature.

## Prerequisites

You need a running OpenClaw instance with at least one channel configured. This skill does NOT manage bot creation or channel connections — OpenClaw handles that. This guide covers the **permissions** your bot needs for each feature to work.

---

## Discord

### 1. Create a Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" → name it → go to "Bot" tab
3. Copy the **Bot Token** → set it in OpenClaw config (`channels.discord.token`)
4. Enable **Privileged Gateway Intents**:
   - `MESSAGE CONTENT INTENT` — required for reading message text
   - `SERVER MEMBERS INTENT` — required for new member onboarding and event detection
   - `PRESENCE INTENT` — optional

### 2. Invite to Server

Generate an invite URL under OAuth2 → URL Generator. Select scopes:
- `bot`
- `applications.commands` (optional, for slash commands)

### 3. Required Permissions by Feature

| Feature | Permissions Needed |
|---------|-------------------|
| FAQ Auto-Reply | `Read Messages` + `Send Messages` + `Read Message History` |
| Daily Digest | `Read Messages` + `Send Messages` + `Read Message History` |
| New Member Onboarding | `Send Messages` + (optional: `Manage Roles` for role assignment) |
| Multilingual Support | `Read Messages` + `Send Messages` |
| Content Moderation | `Read Messages` + `Send Messages` + `Manage Messages` (to delete) |
| Sentiment Analysis | `Read Messages` + `Read Message History` + `Send Messages` |
| Knowledge Extraction | `Read Messages` + `Read Message History` + `Add Reactions` |
| Engagement Gamification | `Read Messages` + `Send Messages` + (optional: `Manage Roles`) |
| Smart Routing | `Read Messages` + `Send Messages` |
| Event Detection | `Read Messages` + `Send Messages` + `Manage Channels` (for slowmode) |
| Scheduled Announcements | `Send Messages` |
| Thread Tracker | `Read Messages` + `Read Message History` + `Send Messages` |

### 4. Recommended Bot Permission Integer

For full functionality, use permission integer **`17448306688`** which includes:
- Read Messages/View Channels
- Send Messages
- Manage Messages
- Manage Roles
- Manage Channels
- Read Message History
- Add Reactions
- Embed Links

### 5. Minimal Permission Integer

For read-only features (FAQ, digest, sentiment, tracker) only: **`68608`**
- Read Messages/View Channels
- Send Messages
- Read Message History

---

## Telegram

### 1. Create a Bot

1. Open Telegram, find **@BotFather**
2. Send `/newbot` → follow prompts → get your **Bot Token**
3. Set the token in OpenClaw config (`channels.telegram.token`)

### 2. Critical: Disable Privacy Mode

```
/setprivacy → Select your bot → Disabled
```

**Why this matters:**
- Privacy mode **Enabled** (default): Bot can ONLY see messages that:
  - Start with `/` (commands)
  - Mention the bot with `@botname`
  - Are replies to the bot's own messages
- Privacy mode **Disabled**: Bot can see ALL messages in the group

If you skip this step, the following features will NOT work:
- FAQ Auto-Reply (can't see questions)
- Daily Digest (can't read messages)
- Sentiment Analysis (no data)
- Knowledge Extraction (can't detect good answers)
- Smart Routing (can't classify questions)
- Thread Tracker (can't find questions)

### 3. Add Bot to Group and Set as Admin

1. Add the bot to your group/supergroup
2. Go to Group Settings → Administrators → Add Administrator → Select your bot
3. Enable permissions:

| Permission | Required For | Recommended |
|------------|-------------|-------------|
| Delete messages | Content Moderation | Yes |
| Ban users | Event Detection (raid response) | Optional |
| Pin messages | Scheduled Announcements | Optional |
| Invite users via link | — | No |
| Remain anonymous | — | No |
| Manage video chats | — | No |
| Add new admins | — | No |

### 4. Minimal Setup (Read-Only Features)

If you only want FAQ, digest, sentiment, and tracker (no moderation):
1. Disable privacy mode (required)
2. Add bot to group (no admin needed)
3. That's it — non-admin bots can read messages and send replies

### 5. Supergroup vs Regular Group

- **Supergroup** (recommended): supports message history, pinning, slowmode, admin granularity
- **Regular group**: limited to 200 members, no granular admin permissions

Telegram auto-upgrades groups to supergroups when you enable admin features. This is fine and expected.

---

## Slack

### 1. Create a Slack App

1. Go to [Slack API](https://api.slack.com/apps) → Create New App
2. Choose "From scratch" → name it → select workspace

### 2. Configure OAuth Scopes

Under **OAuth & Permissions**, add these **Bot Token Scopes**:

| Scope | Required For |
|-------|-------------|
| `channels:history` | Reading messages (public channels) |
| `channels:read` | Listing channels |
| `groups:history` | Reading messages (private channels) |
| `groups:read` | Listing private channels |
| `chat:write` | Sending messages |
| `reactions:read` | Knowledge extraction, gamification |
| `reactions:write` | Adding reactions |
| `users:read` | User info for onboarding, leaderboard |
| `pins:read` | Knowledge extraction |
| `pins:write` | Announcements |

### 3. Install to Workspace

1. Click "Install to Workspace" → Authorize
2. Copy the **Bot User OAuth Token** (`xoxb-...`)
3. Set in OpenClaw config (`channels.slack.token`)

### 4. Invite Bot to Channels

The bot must be explicitly invited to each channel:
```
/invite @your-bot-name
```

Unlike Discord, Slack bots cannot see channels they haven't been invited to, even with correct scopes.

---

## Permission Matrix Summary

Quick reference — minimum permissions per feature across all platforms:

| Feature | Discord | Telegram | Slack |
|---------|---------|----------|-------|
| FAQ Auto-Reply | Read + Send | Privacy OFF | channels:history + chat:write |
| Daily Digest | Read + History + Send | Privacy OFF | channels:history + chat:write |
| Onboarding | Send + (Manage Roles) | Send | chat:write + users:read |
| Moderation | Manage Messages | Admin: Delete msgs | chat:write (no delete in Slack) |
| Sentiment | Read + History | Privacy OFF | channels:history |
| Knowledge | Read + Reactions | Privacy OFF | reactions:read + pins:read |
| Gamification | Read + Send + (Roles) | Privacy OFF | reactions:read + users:read |
| Smart Routing | Read + Send | Privacy OFF + Send | channels:history + chat:write |
| Event Detection | Read + Manage Channels | Admin: Ban users | channels:history + chat:write |
| Announcements | Send | (Admin: Pin) | chat:write + pins:write |
| Thread Tracker | Read + History + Send | Privacy OFF | channels:history + chat:write |

---

## Troubleshooting

### Bot doesn't respond to messages
- **Discord**: Check that `MESSAGE CONTENT INTENT` is enabled in Developer Portal
- **Telegram**: Check that `/setprivacy` is set to `Disabled`
- **Slack**: Check that the bot has been `/invite`'d to the channel

### Bot can't delete messages
- **Discord**: Bot role must be ABOVE the target user's highest role in the role hierarchy
- **Telegram**: Bot must be group admin with "Delete messages" permission
- **Slack**: Slack does not allow bots to delete other users' messages (only their own)

### Bot can't assign roles (Discord)
- Bot's role must be HIGHER than the role it's trying to assign in Server Settings → Roles
- Drag the bot's role above the target roles in the role list
