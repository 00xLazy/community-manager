---
name: community-manager
description: >
  AI-powered community management for Discord, Telegram, and Slack.
  Use when: managing a community, answering repeated questions, generating daily
  channel digests/summaries, onboarding new members, moderating content,
  handling multilingual conversations, tracking community sentiment, extracting
  knowledge from conversations, gamifying engagement, routing questions to the
  right channel, detecting raids or anomalies, scheduling announcements,
  tracking unanswered threads, generating discussion topics, matching mentors
  with newcomers, running polls, managing AMA sessions, creating community
  challenges, building member profiles, generating community health reports,
  or bridging multilingual channels. Triggers on phrases like "manage the
  community", "answer FAQs", "summarize today's chat", "welcome new members",
  "moderate the channel", "community digest", "community sentiment",
  "knowledge base", "leaderboard", "route this question", "detect raid",
  "schedule announcement", "unanswered questions", "thread tracker",
  "start a discussion", "find me a mentor", "run a poll", "start AMA",
  "community challenge", "member profile", "community health", "translate
  channel".
metadata:
  openclaw:
    emoji: "🦐"
---

# Community Manager

Automate community operations across Discord, Telegram, and Slack channels.

**Before using this skill**, ensure your OpenClaw bot has the correct permissions in each platform. See [references/setup-guide.md](references/setup-guide.md) for step-by-step setup instructions, required permissions per feature, and troubleshooting.

## Capabilities

1. **FAQ Auto-Reply** — detect repeated questions and answer from a knowledge base
2. **Daily Digest** — summarize the day's conversations and post to a designated channel
3. **New Member Onboarding** — welcome newcomers with rules and resources
4. **Multilingual Support** — detect language and reply accordingly
5. **Content Moderation** — flag or remove spam, ads, and policy violations
6. **Sentiment Analysis** — track community mood and alert on negative shifts
7. **Knowledge Extraction** — capture high-quality answers into a persistent knowledge base
8. **Engagement Gamification** — leaderboards, contribution tracking, and role rewards
9. **Smart Routing** — auto-route questions to the correct channel
10. **Event Detection** — detect raids, spam waves, and anomalous activity
11. **Scheduled Announcements** — timed, recurring, cross-channel announcements
12. **Thread Tracker** — monitor unanswered questions and stale threads
13. **AI Conversation Starter** — generate discussion topics to keep the community active
14. **Mentor Matching** — pair newcomers with experienced members by expertise
15. **Polls & Surveys** — create and manage community polls with auto-summarized results
16. **AMA Mode** — structured Ask-Me-Anything sessions with question queuing
17. **Community Challenges** — gamified quests and missions for members
18. **Member Profiles** — auto-generated expertise profiles based on activity
19. **Community Health Dashboard** — comprehensive metrics and trend reports
20. **Multilingual Bridge** — real-time translation bridge between language-specific channels

---

## 1. FAQ Auto-Reply

Detect common questions and respond using a curated knowledge base.

### Setup

Create a FAQ knowledge base file (JSON) the bot can reference:

```json
{
  "faqs": [
    {
      "patterns": ["how do I install", "installation guide", "setup instructions"],
      "answer": "Check our getting-started guide: https://example.com/docs/install"
    },
    {
      "patterns": ["pricing", "how much", "cost"],
      "answer": "We offer a free tier and paid plans starting at $9/mo. Details: https://example.com/pricing"
    }
  ]
}
```

Store this file at a known path (e.g., `~/.openclaw/community/faq.json`).

### Workflow

1. Read incoming message content
2. Match against FAQ patterns (fuzzy match — semantic similarity, not just keyword)
3. If match confidence is high: reply with the answer directly in the channel
4. If match confidence is low: do NOT reply; optionally log the question for the admin to review
5. Always attribute the source when answering

### Example — Discord

```bash
# Read recent messages from a channel
message read --channel discord --channelId "123456789" --limit 10

# Send an FAQ answer
message send --channel discord --to "channel:123456789" --text "Great question! Here's our install guide: https://example.com/docs/install"
```

### Example — Telegram

```bash
message send --channel telegram --to "chat:-100123456" --text "Check our docs: https://example.com/docs/install"
```

### Guidelines

- Do NOT answer if unsure — silence is better than a wrong answer
- Prefix AI answers with a subtle indicator (e.g., "🤖 " or "[Auto-Reply]")
- If the same question appears 3+ times in a week and is not in the FAQ, suggest the admin add it
- See [references/faq-guide.md](references/faq-guide.md) for the full FAQ configuration guide

---

## 2. Daily Digest

Summarize the day's conversations and post a digest.

### Workflow

1. At the configured time (or on-demand via "summarize today"), read messages from the last 24 hours
2. Run `scripts/digest.py` or use LLM to generate a structured summary
3. Post the digest to the designated summary channel

### Digest Format

```
📋 Daily Digest — 2026-03-09

🔥 Hot Topics:
• [Topic 1]: brief summary (15 messages)
• [Topic 2]: brief summary (8 messages)

❓ Unanswered Questions:
• "How do I configure X?" — asked by @user1
• "Is Y supported?" — asked by @user2

📊 Stats:
• Messages: 142 | Active members: 23 | New members: 3
```

### Commands

```bash
# Read today's messages
message search --channel discord --channelId "123456789" --query "*" --after "2026-03-09T00:00:00Z"

# Generate digest with script
python3 scripts/digest.py --input messages.json --output digest.md

# Post digest
message send --channel discord --to "channel:DIGEST_CHANNEL_ID" --text "$(cat digest.md)"
```

See [references/daily-digest.md](references/daily-digest.md) for advanced configuration.

---

## 3. New Member Onboarding

Automatically welcome new members and guide them through community resources.

### Workflow

1. Detect new member join event
2. Send a welcome DM or in-channel greeting
3. Share key resources: rules, FAQ channel, introduction channel
4. Optionally assign a default role (Discord)

### Welcome Message Template

```
👋 Welcome to [Community Name], {username}!

Here's how to get started:
1. 📜 Read our community rules: #rules
2. 💬 Introduce yourself in #introductions
3. ❓ Got questions? Check #faq or just ask here

We're glad you're here!
```

### Commands

```bash
# Send welcome DM (Discord)
message send --channel discord --to "user:USER_ID" --text "Welcome message here..."

# Send in-channel welcome (Telegram)
message send --channel telegram --to "chat:-100123456" --text "Welcome @newuser! ..."

# Assign role (Discord — requires bot permissions)
# Use the discord API via bash if role assignment is needed
```

### Guidelines

- Keep welcome messages concise — no walls of text
- Personalize with the member's username
- Do NOT DM if the community prefers public welcomes (configurable)
- Rate-limit: if 10+ members join simultaneously (raid), switch to a single batch welcome

---

## 4. Multilingual Support

Detect the language of incoming messages and reply in the same language.

### Workflow

1. Detect the language of the incoming message (use LLM detection)
2. If a FAQ match exists, translate the answer to the detected language
3. Reply in the user's language
4. For digest summaries: generate in the community's primary language, with a translation available on request

### Guidelines

- Default community language should be configured (e.g., English)
- Only auto-translate when the incoming message is clearly in a different language
- For short messages (< 5 words), default to community language to avoid false detection
- Supported: any language the underlying LLM supports

---

## 5. Content Moderation

Flag or remove messages that violate community policies.

### Workflow

1. Scan incoming messages for policy violations
2. Categorize: spam, advertising, hate speech, NSFW, phishing links
3. Take action based on severity:
   - **Low** (borderline): log for admin review, do nothing publicly
   - **Medium** (likely violation): reply with a warning, notify admin
   - **High** (clear violation): delete message, warn user, notify admin

### Commands

```bash
# Delete a message (Discord)
message delete --channel discord --channelId "123456789" --messageId "MSG_ID"

# Send a warning
message send --channel discord --to "channel:123456789" --text "⚠️ @user, this message was removed for violating our community guidelines."

# Log to admin channel
message send --channel discord --to "channel:ADMIN_CHANNEL_ID" --text "🚨 Moderation alert: message from @user deleted. Reason: spam. Original: ..."
```

### Guidelines

- NEVER auto-delete without high confidence — false positives destroy trust
- Always log moderation actions with the original message content for admin review
- Escalate ambiguous cases to human moderators
- Do NOT moderate admin/moderator messages
- See [references/moderation-policies.md](references/moderation-policies.md) for policy templates

---

## 6. Sentiment Analysis

Track the emotional tone of community conversations and alert on negative shifts.

### Workflow

1. Analyze incoming messages for sentiment (positive / neutral / negative)
2. Maintain a rolling sentiment score per channel (last 1h, 24h, 7d)
3. If sentiment drops sharply (e.g., >30% negative in 1h), alert admin
4. Include sentiment trends in the daily digest

### Alert Format

```
🔴 Sentiment Alert — #general

Mood shifted negative in the last hour.
• Negative messages: 18/25 (72%)
• Key themes: "broken update", "can't login", "bug"
• Likely cause: recent v2.1 release issues

Recommended: post an acknowledgment in #general
```

### Commands

```bash
# Analyze sentiment with LLM (pass recent messages as context)
# LLM prompt: "Rate each message as positive/neutral/negative and provide an overall summary"

# Alert admin
message send --channel discord --to "channel:ADMIN_CHANNEL_ID" --text "🔴 Sentiment alert: ..."
```

### Guidelines

- Use a sliding window, not individual messages — one negative message is not an alert
- Track sentiment by channel, not globally — #support will always be more negative than #random
- See [references/sentiment-tracking.md](references/sentiment-tracking.md) for scoring methodology

---

## 7. Knowledge Extraction

Automatically identify high-quality answers and archive them into the knowledge base.

### Workflow

1. Monitor conversations for signals of a good answer:
   - Reactions (thumbs up, heart, star)
   - Replies like "thanks", "that worked", "perfect"
   - Admin/mod explicit markup: "!save" or emoji reaction (e.g., 📌)
2. Extract the Q&A pair (question + answer)
3. Format and append to the FAQ knowledge base
4. Notify admin: "New knowledge captured: '{topic}' — review and confirm?"

### Extraction Format

```json
{
  "id": "auto-extracted-001",
  "question": "How do I reset my API key?",
  "answer": "Go to Settings > API > Regenerate. Your old key will be invalidated immediately.",
  "source": {
    "channel": "#support",
    "author": "helpful_user",
    "date": "2026-03-09",
    "message_id": "123456"
  },
  "status": "pending_review"
}
```

### Guidelines

- Extracted knowledge is always `pending_review` — admin must confirm before it goes live
- De-duplicate: check if a similar FAQ already exists before adding
- Preserve attribution — credit the original answerer
- See [references/knowledge-extraction.md](references/knowledge-extraction.md) for detection heuristics

---

## 8. Engagement Gamification

Track member contributions and reward active community members.

### Metrics Tracked

- **Questions answered**: replied to a question that got a "thanks" or positive reaction
- **Resources shared**: posted helpful links, guides, or code snippets
- **New member helped**: first responder to a newcomer's question
- **Content created**: started a discussion thread that got 5+ replies

### Leaderboard Format

```
🏆 Weekly Leaderboard — Mar 3-9, 2026

1. 🥇 @alice — 42 pts (15 answers, 3 guides shared)
2. 🥈 @bob — 38 pts (12 answers, 5 newcomers helped)
3. 🥉 @carol — 29 pts (10 answers, 2 threads started)

🌟 Rising Star: @dave (most improved this week)
```

### Commands

```bash
# Post weekly leaderboard
message send --channel discord --to "channel:GENERAL_ID" --text "🏆 Weekly Leaderboard ..."

# Assign role (Discord)
# Use Discord API to assign "Top Helper" role to #1
```

### Guidelines

- Post leaderboard weekly (e.g., every Monday at 10:00)
- Only count genuine contributions — filter out spam/low-effort messages
- Rotate "Rising Star" to encourage new participants
- Make it opt-out: members can disable tracking with a command

---

## 9. Smart Routing

Automatically detect question type and route to the appropriate channel.

### Workflow

1. Detect that a message is a question (heuristic + LLM)
2. Classify the topic: technical, billing, general, feedback, bug report
3. If posted in the wrong channel, suggest redirection:

```
💡 Hey @user, this looks like a billing question!
You'll get faster help in #billing — want me to repost it there?
```

4. If the user confirms (reaction or reply), repost the message in the target channel

### Routing Rules

Configure in `config.json`:

```json
{
  "routing": {
    "technical": "SUPPORT_CHANNEL_ID",
    "billing": "BILLING_CHANNEL_ID",
    "bug_report": "BUGS_CHANNEL_ID",
    "feedback": "FEEDBACK_CHANNEL_ID",
    "general": null
  }
}
```

### Guidelines

- Only suggest routing, never force-move messages
- Don't route if the message is in the correct channel already
- Don't route short/casual messages — only clear questions
- Max 1 routing suggestion per user per hour (avoid annoyance)

---

## 10. Event Detection

Detect anomalous community events and trigger protective measures.

### Monitored Events

| Event | Detection | Action |
|-------|-----------|--------|
| **Raid** | 10+ new accounts join within 5 min | Alert admin, suggest slowmode |
| **Spam wave** | 5+ identical messages from different users | Auto-delete, alert admin |
| **Keyword spike** | Sudden burst of a specific keyword | Alert admin with context |
| **Mass leave** | 10+ members leave within 1 hour | Alert admin |
| **Link flood** | 10+ unique links posted in 5 min by new accounts | Auto-delete, alert admin |

### Commands

```bash
# Run event detector
python3 scripts/event_detector.py --input recent_events.json --thresholds thresholds.json

# Alert admin
message send --channel discord --to "channel:ADMIN_CHANNEL_ID" --text "🚨 Raid detected: 15 new accounts in 3 minutes. Recommend enabling slowmode."

# Enable slowmode (Discord API via bash)
curl -X PATCH "https://discord.com/api/v10/channels/CHANNEL_ID" \
  -H "Authorization: Bot TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"rate_limit_per_user": 30}'
```

### Guidelines

- Detection thresholds should be configurable per community size
- Always alert first, auto-act only for high-confidence events (spam wave, link flood)
- Log all detected events for post-incident review
- See `scripts/event_detector.py` for the detection engine

---

## 11. Scheduled Announcements

Pre-schedule and automate recurring community announcements.

### Workflow

1. Admin creates an announcement via command or config file
2. At the scheduled time, post to the specified channel(s)
3. Support one-time and recurring schedules

### Schedule Format

Configure in `~/.openclaw/community/announcements.json`:

```json
{
  "announcements": [
    {
      "id": "weekly-ama",
      "text": "🎙️ Reminder: Weekly AMA starts in 1 hour in #ama! Bring your questions.",
      "channels": ["discord:CHANNEL_ID", "telegram:CHAT_ID"],
      "schedule": "cron:0 9 * * 1",
      "enabled": true
    },
    {
      "id": "release-note",
      "text": "🚀 v2.2 is live! Check the changelog: https://example.com/changelog",
      "channels": ["discord:ANNOUNCEMENTS_ID"],
      "schedule": "once:2026-03-15T10:00:00Z",
      "enabled": true
    }
  ]
}
```

### Commands

```bash
# Post to multiple channels
message send --channel discord --to "channel:CHANNEL_ID" --text "announcement text"
message send --channel telegram --to "chat:CHAT_ID" --text "announcement text"
```

### Guidelines

- Cross-channel announcements should be sent near-simultaneously
- Support cron syntax for recurring schedules
- Admin can enable/disable announcements without deleting them
- Include a preview command: "show me next week's scheduled announcements"

---

## 12. Thread Tracker

Monitor unanswered questions and stale threads to ensure nothing falls through the cracks.

### Workflow

1. Track all messages identified as questions (from FAQ module or heuristic detection)
2. Mark as "answered" when a substantive reply appears (not just "me too" or reactions)
3. If unanswered after configured timeout (default: 24h), alert admin
4. Generate a periodic "open questions" report

### Alert Format

```
📋 Unanswered Questions Report

⏰ Overdue (>24h):
• "How do I configure SSO?" — @user1 in #support (36h ago)
• "Is there a Python SDK?" — @user2 in #dev (28h ago)

⚠️ Approaching deadline (>12h):
• "Can I use custom domains?" — @user3 in #general (14h ago)

✅ Recently resolved: 5 questions answered today
```

### Commands

```bash
# Run thread tracker
python3 scripts/thread_tracker.py --input messages.json --timeout 24

# Post report
message send --channel discord --to "channel:ADMIN_CHANNEL_ID" --text "$(cat open_questions.md)"
```

### Guidelines

- Only track genuine questions, not rhetorical ones
- A question is "answered" when the asker reacts positively or says thanks
- Don't nag publicly — send overdue alerts to admin channel only
- Include a direct link/reference to the original message for quick navigation
- See `scripts/thread_tracker.py` for the tracking engine

---

## 13. AI Conversation Starter

Generate engaging discussion topics to keep the community active during quiet periods.

### Workflow

1. Monitor channel activity — if no messages in the last N hours, trigger
2. Analyze recent conversation history to understand community interests
3. Generate a relevant, thought-provoking discussion prompt
4. Post to the appropriate channel

### Topic Types

- **This or That**: "Tabs or spaces? And more importantly, why?"
- **Hot Take**: "Controversial opinion: monorepos are always better. Agree or disagree?"
- **Show & Tell**: "What side project are you working on this weekend?"
- **Hypothetical**: "If you could mass-delete one programming concept, what would it be?"
- **Retrospective**: "What's the best thing you learned this week?"
- **Community-specific**: Based on recent trending topics in the community

### Commands

```bash
# Generate a topic based on community context
# LLM prompt: "Based on these recent conversations, generate an engaging discussion topic..."

# Post the discussion starter
message send --channel discord --to "channel:GENERAL_ID" --text "💬 Discussion Time!\n\n{topic}\n\nDrop your thoughts below 👇"
```

### Guidelines

- Max 1 conversation starter per day per channel
- Never post during active conversations — only during quiet periods (configurable, default 4h silence)
- Vary topic types to keep things fresh
- If a topic gets no engagement (< 3 replies), try a different style next time
- See [references/conversation-starters.md](references/conversation-starters.md) for topic templates

---

## 14. Mentor Matching

Pair newcomers with experienced community members based on interests and expertise.

### Workflow

1. New member joins and introduces themselves (or fills out a profile via DM)
2. Analyze their interests, background, and goals
3. Match with an experienced member who has expertise in those areas
4. Suggest the pairing to both parties via DM

### Matching Format

```
🤝 Mentor Match Suggestion

Hey @alice! We think @bob would be a great mentor for you:

🎯 Your interests: React, TypeScript, frontend
⭐ @bob's expertise: React (42 answers), TypeScript (28 answers), CSS (15 answers)
📊 @bob's helpfulness score: 4.8/5.0

Want to connect? React ✅ and we'll introduce you two!
```

### Mentor Criteria

- Has been in the community > 30 days
- Has answered > 10 questions
- Has positive sentiment ratio > 0.7
- Has opted in to mentoring (via `!mentor on` command)

### Commands

```bash
# DM the newcomer
message send --channel discord --to "user:NEWCOMER_ID" --text "🤝 Mentor Match: ..."

# DM the mentor
message send --channel discord --to "user:MENTOR_ID" --text "👋 You've been suggested as a mentor for @newcomer..."

# If both accept, create an introduction
message send --channel discord --to "channel:INTRODUCTIONS_ID" --text "🎉 @newcomer, meet @mentor! ..."
```

### Guidelines

- Mentors must opt-in — never assign without consent
- Max 3 active mentees per mentor (prevent burnout)
- Follow up after 1 week: "How's the mentorship going?"
- See [references/mentor-matching.md](references/mentor-matching.md) for matching algorithm

---

## 15. Polls & Surveys

Create, manage, and auto-summarize community polls.

### Workflow

1. Admin or user requests a poll: "run a poll: what feature should we build next?"
2. Generate poll options (from user input or AI-suggested)
3. Post poll with reaction-based or button-based voting
4. Auto-close after configured duration
5. Summarize and announce results

### Poll Formats

**Quick Poll (reaction-based):**
```
📊 Quick Poll: What should we focus on next?

1️⃣ Better documentation
2️⃣ More integrations
3️⃣ Performance improvements
4️⃣ Mobile app

React to vote! Poll closes in 24h.
```

**Detailed Survey (multi-question):**
```
📋 Community Survey — Q1 2026

DM me your answers (reply with numbers):

1. How satisfied are you with our docs? (1-5)
2. What's your most-used feature?
3. What would you change if you could?

Survey closes: March 15
```

### Result Summary

```
📊 Poll Results: "What should we focus on next?"

🏆 Winner: Better documentation (42 votes, 38%)
  2. More integrations (31 votes, 28%)
  3. Performance improvements (24 votes, 22%)
  4. Mobile app (13 votes, 12%)

Total votes: 110 | Participation: 23% of active members
💡 AI insight: Documentation was the top request — consider starting a docs sprint.
```

### Commands

```bash
# Post poll (Discord supports native polls)
message poll --channel discord --to "channel:GENERAL_ID" --question "What should we focus on next?" --options '["Better docs","More integrations","Performance","Mobile app"]' --duration 24h

# Summarize results
message send --channel discord --to "channel:GENERAL_ID" --text "📊 Poll Results: ..."
```

### Guidelines

- Max 1 active poll per channel
- Default duration: 24 hours (configurable)
- Include an AI-generated insight with results
- Anonymous by default — don't expose who voted what

---

## 16. AMA Mode

Structured Ask-Me-Anything sessions with question queuing and moderation.

### Workflow

1. Admin starts AMA: "start AMA with @guest in #ama"
2. Bot enters AMA mode: collects questions, manages queue, prevents off-topic noise
3. Present questions one at a time to the guest
4. Guest answers, bot queues the next question
5. Auto-generate summary when AMA ends

### AMA Flow

**Start:**
```
🎙️ AMA Session Started!

Guest: @guest_name — CTO of ExampleCo
Topic: Building scalable microservices

📝 How to participate:
• Submit questions by replying to this message
• Questions will be queued and presented one at a time
• Use 👍 on other questions to upvote them
• Top-voted questions go first

Type !endama to end the session.
```

**During (presenting a question):**
```
❓ Question #3 (from @user, 12 upvotes):
"How do you handle database migrations in a microservices architecture?"

@guest_name, the floor is yours!
```

**End Summary:**
```
📋 AMA Summary — @guest_name

⏱️ Duration: 1h 23m
❓ Questions answered: 15/22
👥 Participants: 47

Top Q&A:
1. "How do you handle DB migrations?" — "We use a saga pattern with..."
2. "What's your tech stack?" — "We run on..."
3. "Hiring advice?" — "Look for people who..."

Full transcript: [link]
```

### Commands

```bash
# Start AMA
message send --channel discord --to "channel:AMA_CHANNEL_ID" --text "🎙️ AMA Session Started! ..."

# Present next question
message send --channel discord --to "channel:AMA_CHANNEL_ID" --text "❓ Question #3: ..."

# End and summarize
message send --channel discord --to "channel:AMA_CHANNEL_ID" --text "📋 AMA Summary: ..."
```

### Guidelines

- Only admins/mods can start and end AMA sessions
- Sort questions by upvotes (most popular first)
- Filter duplicate/similar questions automatically
- Mute non-question messages during AMA (optional, configurable)
- Save transcript for future reference

---

## 17. Community Challenges

Gamified missions and quests to drive engagement and learning.

### Challenge Types

**Daily Challenge:**
```
🎯 Daily Challenge — March 10, 2026

"Share one useful tool or resource you discovered recently"

Reward: 10 pts + 🌟 Curator badge
Time limit: 24 hours
```

**Weekly Quest:**
```
⚔️ Weekly Quest — Week of March 9

"Answer 5 questions in #support this week"

Progress: ██████░░░░ 3/5
Reward: 50 pts + 🛡️ Support Hero badge
```

**Community Goal (collaborative):**
```
🌍 Community Goal — March 2026

"Collectively answer 500 questions this month"

Progress: ████████░░ 412/500 (82%)
Top contributors: @alice (45), @bob (38), @carol (31)
Reward: Everyone gets 🏅 Community Champion badge
```

### Commands

```bash
# Post daily challenge
message send --channel discord --to "channel:GENERAL_ID" --text "🎯 Daily Challenge: ..."

# Update quest progress
message send --channel discord --to "channel:GENERAL_ID" --text "⚔️ Quest Update: @user completed step 3/5!"

# Announce community goal progress
message send --channel discord --to "channel:GENERAL_ID" --text "🌍 Community Goal: 82% complete!"
```

### Guidelines

- Vary challenge difficulty — mix easy wins with stretch goals
- Challenges should drive genuine value (not spam)
- Collaborative goals build community spirit — use them often
- See [references/community-challenges.md](references/community-challenges.md) for challenge templates

---

## 18. Member Profiles

Auto-generate expertise profiles for active members based on their activity.

### Profile Format

```
👤 Member Profile — @alice

📅 Joined: 6 months ago
💬 Messages: 1,234
⭐ Reputation: 4.8/5.0

🏅 Badges:
• 🥇 Top Helper (3x weekly champion)
• 🛡️ Support Hero (50+ questions answered)
• 📚 Knowledge Curator (10+ FAQs contributed)

📊 Expertise Areas:
• React/TypeScript ████████░░ (strong — 42 answers)
• Node.js         ██████░░░░ (moderate — 28 answers)
• DevOps          ████░░░░░░ (growing — 15 answers)

🔥 Recent Activity:
• Answered 8 questions this week
• Contributed 2 knowledge base entries
• Started 1 popular discussion (23 replies)
```

### How It Works

1. Track all member interactions: questions asked, answers given, reactions received
2. Classify topics of answers/discussions using LLM
3. Build an expertise vector per member
4. Generate profile on request ("show me @alice's profile") or periodically
5. Store profiles in `~/.openclaw/community/profiles/`

### Commands

```bash
# Generate and send profile
message send --channel discord --to "user:USER_ID" --text "👤 Your Profile: ..."

# Post monthly top profiles
message send --channel discord --to "channel:GENERAL_ID" --text "🌟 Member Spotlight: ..."
```

### Guidelines

- Profiles are public by default — members can opt-out
- Update profiles weekly, not in real-time (reduce noise)
- Use profiles for mentor matching (module 14) and smart routing (module 9)
- "Member Spotlight" — feature one outstanding member per month

---

## 19. Community Health Dashboard

Generate comprehensive community health reports with actionable insights.

### Report Format

```
📊 Community Health Report — Week of March 3-9, 2026

🌡️ Overall Health Score: 87/100 (↑3 from last week)

📈 Growth:
• New members: 23 (↑15%)
• Member retention: 94%
• Active members: 156/420 (37%)

💬 Engagement:
• Messages: 2,341 (↑8%)
• Avg response time: 12 min (↓3 min, improving!)
• Questions answered: 89% (↑2%)
• Most active channel: #general (534 msgs)
• Quietest channel: #off-topic (12 msgs)

😊 Sentiment:
• Overall: 0.72 (positive)
• Trend: stable
• Happiest channel: #showcase (0.91)
• Needs attention: #support (0.45)

🏆 Top Contributors:
• @alice (42 helpful answers)
• @bob (38 questions answered)
• @carol (29 resources shared)

⚠️ Action Items:
• #support sentiment is declining — consider adding more moderators
• 11 questions went unanswered for >48h — review thread tracker
• #dev channel has low engagement — try a discussion starter
```

### Commands

```bash
# Generate health report using script
python3 scripts/health_report.py --input activity.json --period weekly

# Post report
message send --channel discord --to "channel:ADMIN_CHANNEL_ID" --text "$(cat health_report.md)"
```

### Guidelines

- Generate weekly (Monday morning) and monthly (1st of month)
- Health score formula: weighted average of engagement, sentiment, retention, response time
- Include actionable recommendations, not just data
- Compare against previous period — trends matter more than absolutes
- See `scripts/health_report.py` for the report generator

---

## 20. Multilingual Bridge

Real-time translation bridge between language-specific channels.

### Workflow

1. User posts in `#chinese` in Chinese
2. Bot detects the language and translates using LLM
3. Bot cross-posts the translated message to `#english` (and vice versa)
4. Replies are tracked and bridged back

### Bridge Format

**In #english:**
```
🌐 [#chinese] @wang_wei:
"Has anyone tested the new API endpoint? I'm getting a 403 error with the v2 token."

(Original: 有人测试过新的API端点吗？我用v2 token总是收到403错误。)

💬 Reply here — your response will be translated back to #chinese
```

**In #chinese (when someone replies in #english):**
```
🌐 [#english] @alice:
"是的，v2 token需要在header里加上 X-API-Version: 2。这是文档链接：..."

(Original: Yes, the v2 token requires adding X-API-Version: 2 in the header. Here's the doc link: ...)
```

### Configuration

```json
{
  "bridges": [
    {
      "channels": ["ENGLISH_CHANNEL_ID", "CHINESE_CHANNEL_ID"],
      "languages": ["en", "zh"]
    },
    {
      "channels": ["ENGLISH_CHANNEL_ID", "JAPANESE_CHANNEL_ID"],
      "languages": ["en", "ja"]
    }
  ]
}
```

### Commands

```bash
# Cross-post translated message
message send --channel discord --to "channel:TARGET_CHANNEL_ID" --text "🌐 [#source] @user:\n\"translated text\"\n\n(Original: original text)"
```

### Guidelines

- Always show the original text alongside translation for transparency
- Include sender attribution and source channel
- Bridge replies back to the original channel
- Skip messages that are already in the target language
- Don't bridge bot messages or system messages (prevent loops)
- Short messages (emojis, "ok", "thanks") don't need translation

---

## Configuration

The skill reads configuration from `~/.openclaw/community/config.json`:

```json
{
  "community_name": "My Community",
  "primary_language": "en",
  "channels": {
    "discord": {
      "guild_id": "...",
      "faq_channel": "...",
      "digest_channel": "...",
      "admin_channel": "...",
      "welcome_channel": "..."
    },
    "telegram": {
      "chat_id": "..."
    }
  },
  "features": {
    "faq": true,
    "digest": true,
    "onboarding": true,
    "multilingual": true,
    "moderation": true,
    "sentiment": true,
    "knowledge_extraction": true,
    "gamification": true,
    "smart_routing": true,
    "event_detection": true,
    "announcements": true,
    "thread_tracker": true,
    "conversation_starter": true,
    "mentor_matching": true,
    "polls": true,
    "ama_mode": true,
    "challenges": true,
    "member_profiles": true,
    "health_dashboard": true,
    "multilingual_bridge": true
  },
  "digest_time": "09:00",
  "moderation_level": "medium",
  "sentiment_alert_threshold": 0.3,
  "thread_timeout_hours": 24,
  "leaderboard_day": "monday",
  "conversation_starter_silence_hours": 4,
  "health_report_day": "monday",
  "routing": {
    "technical": "SUPPORT_CHANNEL_ID",
    "billing": "BILLING_CHANNEL_ID",
    "bug_report": "BUGS_CHANNEL_ID",
    "feedback": "FEEDBACK_CHANNEL_ID"
  },
  "bridges": [
    {
      "channels": ["ENGLISH_CHANNEL_ID", "CHINESE_CHANNEL_ID"],
      "languages": ["en", "zh"]
    }
  ]
}
```

## When NOT to Use

- Private 1-on-1 conversations (this skill is for group/community channels)
- Server administration tasks (creating channels, managing permissions)
- Payment or billing operations
- Anything requiring access to external databases not configured in the FAQ
