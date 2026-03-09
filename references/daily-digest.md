# Daily Digest Workflow

## Overview

Generate and post a structured summary of the day's community activity.

## Trigger Options

1. **Scheduled**: Run at `digest_time` from config (e.g., "09:00" UTC daily)
2. **On-demand**: User says "summarize today" or "community digest"
3. **Weekly**: Optional weekly digest every Monday covering the past 7 days

## Data Collection

### Step 1: Fetch Messages

Read all messages from the target channels within the time window:

```bash
# Discord — read last 24h from a channel
message search --channel discord --channelId "CHANNEL_ID" --after "ISO_TIMESTAMP" --limit 500

# Telegram — read recent messages
message read --channel telegram --chatId "CHAT_ID" --limit 500
```

### Step 2: Filter & Categorize

Group messages by:
- **Topic threads** (Discord threads or reply chains)
- **Question vs discussion** (messages ending with "?" or starting with "how/what/why")
- **Announcements** (messages from admins/mods)
- **Media shares** (links, images, files)

### Step 3: Generate Summary

Use `scripts/digest.py` or LLM directly:

```bash
python3 scripts/digest.py --input messages.json --format markdown
```

## Output Format

```markdown
📋 Daily Digest — {date}

🔥 Hot Topics:
• {topic}: {summary} ({count} messages)

❓ Unanswered Questions:
• "{question}" — @{user}

📊 Activity:
• Messages: {total} | Active: {unique_users} | New: {new_members}

🔗 Shared Links:
• {title}: {url}
```

## Configuration

In `config.json`:

```json
{
  "digest_time": "09:00",
  "digest_channels": ["general", "support", "dev"],
  "digest_target": "DIGEST_CHANNEL_ID",
  "digest_format": "markdown",
  "include_links": true,
  "include_unanswered": true,
  "max_topics": 5
}
```

## Tips

- Keep digest under 2000 characters for Discord (message limit)
- For busy communities (500+ msgs/day), focus on top 5 topics only
- Exclude bot messages from the digest
- If no significant activity, post a short "quiet day" message instead of nothing
