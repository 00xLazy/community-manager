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
  bridging multilingual channels, summarizing long discussions, generating
  throwback posts, managing office hours, coordinating collaborative projects,
  predicting member churn, visualizing member relationships, auto-tagging
  members, re-engaging inactive members, recommending content, maintaining
  community wiki, incentivizing content creation, collecting feedback,
  managing community events, or scheduling admin shifts. Triggers on phrases
  like "manage the community", "answer FAQs", "summarize today's chat",
  "welcome new members", "moderate the channel", "community digest",
  "community sentiment", "knowledge base", "leaderboard", "route this
  question", "detect raid", "schedule announcement", "unanswered questions",
  "thread tracker", "start a discussion", "find me a mentor", "run a poll",
  "start AMA", "community challenge", "member profile", "community health",
  "translate channel", "summarize this thread", "what happened today last
  year", "office hours", "start a project", "who's going inactive",
  "member graph", "tag members", "bring back inactive users", "recommend
  posts", "community wiki", "content creators", "collect feedback",
  "community calendar", "admin schedule".
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
21. **Long Thread Summary** — auto-summarize discussions that exceed a message threshold
22. **Throwback Posts** — "on this day" posts from community history to build nostalgia
23. **Office Hours** — scheduled Q&A sessions with experts, with queue management
24. **Collaborative Projects** — community-driven project boards for team coordination
25. **Churn Prediction** — detect members going inactive and trigger re-engagement
26. **Social Graph** — visualize member relationships and interaction patterns
27. **Smart Tags** — auto-label members by expertise, activity patterns, and contribution type
28. **Win-Back Campaigns** — personalized outreach to re-engage inactive members
29. **Content Recommendation** — suggest relevant historical discussions and resources
30. **Community Wiki** — auto-maintained structured knowledge base from discussions
31. **Content Creator Incentives** — track and reward original tutorials, guides, and posts
32. **Feedback Collector** — aggregate bug reports, feature requests, and suggestions
33. **Community Calendar** — manage events with reminders, RSVPs, and post-event recaps
34. **Admin Shift Scheduler** — automated moderator rotation and workload tracking

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

## 21. Long Thread Summary

Auto-summarize discussions that grow beyond a configurable message threshold.

### Workflow

1. Monitor threads/channels — when a conversation exceeds N messages (default: 50), trigger
2. Use LLM to generate a concise TL;DR covering key points, decisions, and open questions
3. Post the summary as a reply in the thread or pin it
4. Update the summary if the discussion continues significantly

### Summary Format

```
📝 Thread Summary (87 messages)

🔑 Key Points:
• The team agreed to migrate from REST to GraphQL for the v3 API
• @alice proposed a phased rollout over 3 sprints
• Concern raised about backward compatibility with mobile clients

❓ Open Questions:
• Who will own the migration tooling? (no volunteer yet)
• Should we deprecate REST immediately or run both in parallel?

👥 Main Participants: @alice, @bob, @carol, @dave (12 others)
```

### Commands

```bash
# Read thread messages
message read --channel discord --channelId "THREAD_ID" --limit 100

# Post summary
message send --channel discord --to "channel:THREAD_ID" --text "📝 Thread Summary: ..."
```

### Guidelines

- Only summarize when thread exceeds threshold — don't interrupt short discussions
- Include attribution for key contributions
- Distinguish between decisions made and open questions
- Update summary if 20+ new messages arrive after last summary
- Never summarize private/DM conversations

---

## 22. Throwback Posts

Generate "on this day" posts from community history to build nostalgia and highlight milestones.

### Workflow

1. Daily, search message history for the same date in previous months/years
2. Identify notable events: popular discussions, milestones, funny moments
3. Format and post a throwback message

### Throwback Format

```
📅 On This Day — 1 Year Ago

🔥 Hot Discussion: "Should we switch to Rust?"
   → 47 replies, most heated debate of the month!
   → Final consensus: "Maybe next year" 😄

🎉 Milestone: Community hit 1,000 members!

💡 Best Answer: @bob explained WebSocket reconnection
   → Still one of our most-referenced answers

#throwback #community-memories
```

### Commands

```bash
# Search historical messages
message search --channel discord --channelId "GENERAL_ID" --after "2025-03-09T00:00:00Z" --before "2025-03-10T00:00:00Z"

# Post throwback
message send --channel discord --to "channel:GENERAL_ID" --text "📅 On This Day: ..."
```

### Guidelines

- Post max 1 throwback per day (morning, before daily digest)
- Only post if there's genuinely interesting content — skip boring days
- Avoid resurfacing controversial/negative moments
- Start generating throwbacks after the community has at least 3 months of history
- See [references/throwback-posts.md](references/throwback-posts.md) for content selection criteria

---

## 23. Office Hours

Manage structured expert Q&A sessions with queue management and follow-up.

### Workflow

1. Admin schedules office hours: "schedule office hours with @expert every Thursday 2-3pm"
2. Bot announces upcoming office hours and collects pre-submitted questions
3. During the session, manage the question queue (similar to AMA but recurring)
4. After the session, generate a summary and archive Q&A pairs

### Office Hours Format

**Announcement:**
```
🕐 Office Hours — Thursday, March 13

Expert: @alice (Backend Architecture)
Time: 2:00-3:00 PM UTC
Channel: #office-hours

📝 Pre-submit your questions by replying here!
Already queued: 5 questions
```

**During Session:**
```
🟢 Office Hours LIVE — @alice

Current question from @user1:
"What's the best approach for handling distributed transactions?"

⏰ Time remaining: 42 minutes | Questions left: 4
Next up: @user2's question about caching strategies
```

**Summary:**
```
📋 Office Hours Recap — March 13

Expert: @alice | Duration: 58 min
Questions answered: 7/8
Attendees: 23

Top Q&A:
1. Distributed transactions → Saga pattern recommended
2. Caching strategies → Redis + local cache hybrid
3. API versioning → URL-based for public APIs

📌 2 answers added to knowledge base
Next session: March 20, 2:00 PM UTC
```

### Commands

```bash
# Announce office hours
message send --channel discord --to "channel:GENERAL_ID" --text "🕐 Office Hours coming up: ..."

# Manage queue during session
message send --channel discord --to "channel:OFFICE_HOURS_ID" --text "🟢 Current question: ..."
```

### Guidelines

- Office hours are recurring — different from one-off AMAs
- Pre-submitted questions get priority (sorted by upvotes)
- Walk-in questions allowed if time permits
- Auto-extract Q&A pairs to knowledge base after each session
- Send reminder 1 hour and 10 minutes before start

---

## 24. Collaborative Projects

Community-driven project coordination with team formation, progress tracking, and showcasing.

### Workflow

1. Member proposes a project: "!project new Build a community bot dashboard"
2. Bot creates a project thread with roles/skills needed
3. Members join by reacting or commenting
4. Track milestones and progress updates
5. Showcase completed projects

### Project Board Format

```
🚀 Active Community Projects

1. 📦 Community Bot Dashboard
   Lead: @alice | Team: 4/6 members
   Status: ██████░░░░ 60% | Sprint 2/3
   Needs: 1 frontend dev, 1 designer
   Channel: #project-dashboard

2. 📚 Interactive Tutorial Series
   Lead: @bob | Team: 3/3 members
   Status: ████████░░ 80% | Final review
   Channel: #project-tutorials

3. 🌐 Multilingual Docs
   Lead: @carol | Team: 7 members
   Status: ████░░░░░░ 40% | Translating
   Needs: Japanese, Korean translators
   Channel: #project-docs
```

### Commands

```bash
# Post project board
message send --channel discord --to "channel:PROJECTS_ID" --text "🚀 Active Projects: ..."

# Create project thread
message send --channel discord --to "channel:PROJECTS_ID" --text "📦 New Project: ..."
```

### Guidelines

- Each project gets its own thread/channel
- Weekly progress check-in reminders
- Archive inactive projects after 30 days of no updates
- Showcase completed projects in #showcase with a celebration post
- Award "Team Player" badges to participants

---

## 25. Churn Prediction

Detect members at risk of leaving and trigger proactive re-engagement.

### Workflow

1. Track activity patterns for each member: message frequency, reaction frequency, login times
2. Build a baseline for each member (their "normal" activity level)
3. Detect significant drops: member usually posts 5x/day but hasn't posted in 3 days
4. Score churn risk: low / medium / high
5. Alert admin with context and recommended actions

### Alert Format

```
⚠️ Churn Risk Report — Weekly

🔴 High Risk (likely to leave):
• @alice — No activity for 14 days (was posting 5x/day)
  Last active in: #dev | Possible cause: unanswered question on March 1
  Suggested action: personal reach-out from admin

• @bob — Activity dropped 90% over 2 weeks
  Last active in: #general | Possible cause: negative interaction on Feb 28
  Suggested action: check-in DM

🟡 Medium Risk (declining engagement):
• @carol — Activity down 50% this week vs. last month average
• @dave — Stopped reacting to messages (still reading)

📊 Overall: 3% of active members at high churn risk (vs. 2% last week)
```

### Signals Tracked

| Signal | Weight | Description |
|--------|--------|-------------|
| Message frequency drop | High | Fewer messages than personal baseline |
| Reaction stop | Medium | Stopped reacting but may still lurk |
| Channel narrowing | Medium | Active in fewer channels than usual |
| Negative last interaction | High | Last message was negative or unanswered |
| Login without posting | Low | Opening the app but not engaging |

### Commands

```bash
# Generate churn report
# LLM prompt: analyze member activity data and identify at-risk members

# Alert admin
message send --channel discord --to "channel:ADMIN_CHANNEL_ID" --text "⚠️ Churn Risk Report: ..."
```

### Guidelines

- Never publicly flag someone as "at risk" — admin-only alerts
- Focus on previously active members, not lurkers (they have a different pattern)
- Suggest specific actions: DM, mention in a relevant discussion, ask for their opinion
- Track if re-engagement actions worked — learn what brings people back
- See [references/churn-prediction.md](references/churn-prediction.md) for scoring methodology

---

## 26. Social Graph

Visualize and analyze member interaction patterns and community structure.

### Workflow

1. Track who replies to whom, who reacts to whose messages, who co-participates in threads
2. Build an interaction graph with weighted edges
3. Identify clusters (sub-communities), bridges (members who connect clusters), and isolated members
4. Generate insights for community management

### Report Format

```
🕸️ Social Graph Insights — March 2026

🏘️ Community Clusters:
• Frontend Crew (12 members): @alice, @bob, @carol... — centered around #react
• DevOps Guild (8 members): @dave, @eve... — centered around #infrastructure
• Newcomer Group (15 members): loosely connected, mostly in #general

🌉 Bridge Members (connect different groups):
• @alice — links Frontend Crew ↔ DevOps Guild (answers in both)
• @bob — links Frontend Crew ↔ Newcomer Group (active mentor)

🏝️ Isolated Members (active but not connected):
• @frank — posts often but rarely gets replies (consider routing to relevant channels)
• @grace — only interacts with bot, not other members

💡 Recommendations:
• Create a cross-team event to connect Frontend Crew and DevOps Guild
• @frank might benefit from a mentor match
• Consider a "buddy system" for the Newcomer Group
```

### Commands

```bash
# Generate social graph analysis
# LLM prompt: analyze interaction patterns and identify clusters, bridges, isolated members

# Post insights
message send --channel discord --to "channel:ADMIN_CHANNEL_ID" --text "🕸️ Social Graph: ..."
```

### Guidelines

- Generate monthly — social patterns change slowly
- Focus on actionable insights, not raw data
- Never share individual interaction data publicly
- Use graph data to improve mentor matching (module 14) and smart routing (module 9)
- Identify and nurture "bridge" members — they're critical for community cohesion

---

## 27. Smart Tags

Automatically label members based on activity patterns, expertise, and contribution type.

### Workflow

1. Analyze each member's activity: channels frequented, topics discussed, help given
2. Assign tags automatically based on detected patterns
3. Update tags weekly as behavior evolves
4. Use tags for smart routing, mentor matching, and targeted announcements

### Tag Categories

**Expertise Tags** (based on answers given):
```
@alice: [react] [typescript] [frontend] [testing]
@bob: [python] [devops] [docker] [ci-cd]
@carol: [design] [ux] [figma] [accessibility]
```

**Role Tags** (based on behavior):
```
@alice: [helper] [mentor] [early-adopter]
@bob: [creator] [documenter] [bug-reporter]
@carol: [community-builder] [welcomer] [translator]
```

**Activity Tags** (based on patterns):
```
@alice: [night-owl] [weekday-active] [high-frequency]
@bob: [morning-person] [weekend-warrior] [consistent]
@carol: [burst-poster] [deep-diver] [multi-channel]
```

### Use Cases

- **Targeted announcements**: "Notify all [devops] tagged members about the new CI pipeline"
- **Smart routing**: "Route Docker questions to members tagged [docker]"
- **Mentor matching**: Match newcomer interested in React with [react][helper] tagged members
- **Event planning**: Schedule events when [night-owl] or [morning-person] members are active

### Commands

```bash
# Query tagged members
# "Who in the community is tagged [react]?"

# Update tags
# Tags are computed automatically — no manual commands needed

# Use tags for targeting
message send --channel discord --to "channel:DEVOPS_ID" --text "📢 Attention [devops] members: ..."
```

### Guidelines

- Tags are internal/admin-only by default — members can view their own tags
- Members can opt-out of tagging
- Update weekly to reflect evolving activity
- Don't over-tag — max 5 expertise tags, 3 role tags, 3 activity tags per member
- Tags inform other modules but never replace human judgment

---

## 28. Win-Back Campaigns

Personalized outreach to re-engage members who have gone inactive.

### Workflow

1. Identify inactive members (no activity for 14+ days, previously active)
2. Analyze their interests and past contributions
3. Generate a personalized message highlighting what they've missed
4. Send via DM (if allowed) or tagged mention
5. Track response rate and adjust approach

### Message Templates

**For a helper/expert:**
```
👋 Hey @alice, we miss you in the community!

Since you've been away:
• 12 React questions went unanswered that match your expertise
• @bob mentioned your tutorial in a discussion yesterday
• We launched a new #typescript channel you might like

Your contributions really made a difference — 23 people thanked you last month! No pressure, just wanted you to know we're here. 😊
```

**For a social/active member:**
```
👋 Hey @carol, the community hasn't been the same without you!

Here's what you missed:
• 🔥 Hot debate: "Is Tailwind actually good?" (47 replies!)
• 🎉 We hit 500 members!
• 📊 Poll results: TypeScript won as the most-loved tool

Jump back in anytime — #general misses your energy!
```

**For a newcomer who left early:**
```
👋 Hey @dave, just checking in!

We noticed you joined a few weeks ago but haven't been around much. If you had a question that went unanswered, we're sorry!

Here are some ways to get involved:
• 💬 Introduce yourself in #introductions
• ❓ Ask anything in #support — avg response time is 12 min
• 🤝 Want a mentor? Just say "!mentor match me"

We'd love to have you back!
```

### Commands

```bash
# Send win-back DM
message send --channel discord --to "user:USER_ID" --text "👋 Hey @user, we miss you..."

# Log win-back attempt
message send --channel discord --to "channel:ADMIN_CHANNEL_ID" --text "📤 Win-back sent to @user (inactive 21 days)"
```

### Guidelines

- Max 1 win-back message per member per 30 days — don't spam
- Never send to members who opted out of DMs
- Personalize based on their history — generic messages don't work
- Track success rate: did they come back? How long did they stay?
- Escalate to admin for high-value members (top contributors who went silent)
- See [references/winback-campaigns.md](references/winback-campaigns.md) for templates and timing

---

## 29. Content Recommendation

Proactively suggest relevant historical discussions, resources, and content to members.

### Workflow

1. When a member asks a question or discusses a topic, search history for related content
2. If relevant past discussions exist, suggest them alongside or after the answer
3. Periodically post "best of" compilations in relevant channels

### Recommendation Format

**Inline (after answering a question):**
```
💡 Related discussions you might find useful:
• "GraphQL vs REST debate" (Feb 2026, 34 replies) — covers migration strategies
• @alice's guide: "Setting up Apollo Server" (pinned in #dev)
• FAQ: "GraphQL authentication patterns" — from our knowledge base
```

**Weekly "Best Of" Post:**
```
⭐ Best of This Week — Top Community Content

📚 Most Helpful Answers:
1. @bob on database indexing strategies (18 👍)
2. @carol's Docker debugging tips (14 👍)
3. @dave's explanation of JWT refresh tokens (12 👍)

🔥 Most Discussed:
1. "Monorepo tooling in 2026" — 42 replies
2. "AI coding assistants review" — 38 replies

📌 New Knowledge Base Entries: 5 this week
```

### Commands

```bash
# Search for related content
message search --channel discord --channelId "CHANNEL_ID" --query "GraphQL migration" --limit 5

# Post recommendation
message send --channel discord --to "channel:CHANNEL_ID" --text "💡 Related: ..."

# Post weekly best-of
message send --channel discord --to "channel:GENERAL_ID" --text "⭐ Best of This Week: ..."
```

### Guidelines

- Max 1 recommendation per question — don't overwhelm
- Only recommend content with high engagement (5+ reactions or replies)
- "Best of" posts go out weekly, after the digest
- Recommendations improve FAQ matching and reduce repeat questions
- Use member tags (module 27) to personalize recommendations

---

## 30. Community Wiki

Auto-maintain a structured, living knowledge base from community discussions.

### Workflow

1. Aggregate knowledge from: FAQ entries, extracted Q&A pairs, pinned messages, popular discussions
2. Organize into categories/topics automatically using LLM
3. Generate and maintain wiki pages per topic
4. Update pages when new relevant knowledge is captured
5. Provide search interface for members

### Wiki Structure

```
📖 Community Wiki

📂 Getting Started
├── Installation Guide (from FAQ, updated March 9)
├── First Steps Tutorial (from @alice's guide, Feb 15)
└── Common Errors & Fixes (auto-generated from #support, 23 entries)

📂 Architecture
├── API Design Patterns (from office hours with @bob, March 6)
├── Database Selection Guide (from community discussion, 47 replies)
└── Microservices vs Monolith (from AMA with @carol, Feb 20)

📂 DevOps
├── Docker Best Practices (curated from 12 discussions)
├── CI/CD Pipeline Setup (from @dave's tutorial)
└── Monitoring & Alerting (from knowledge base, 8 entries)

Last updated: March 9, 2026 | Total entries: 67
```

### Commands

```bash
# Generate wiki page
# LLM prompt: "Organize these knowledge base entries into a structured wiki page about {topic}"

# Post wiki update notification
message send --channel discord --to "channel:GENERAL_ID" --text "📖 Wiki Updated: 3 new entries in 'Getting Started'"

# Search wiki
# "search wiki for Docker networking"
```

### Guidelines

- Auto-update when new knowledge is extracted (module 7)
- Keep entries concise — link to full discussions for details
- Credit original authors
- Admin can edit/reorganize wiki entries
- Version history: track changes over time
- See [references/community-wiki.md](references/community-wiki.md) for organization schema

---

## 31. Content Creator Incentives

Track, encourage, and reward original content creation (tutorials, guides, blog posts).

### Workflow

1. Detect original content: long-form posts, tutorials, code walkthroughs, guides
2. Track engagement metrics: views, reactions, bookmarks, replies
3. Highlight top content creators on leaderboard
4. Award special badges and recognition

### Content Types Tracked

| Type | Detection | Points |
|------|-----------|--------|
| Tutorial / Guide | 500+ chars, step-by-step format | 30 pts |
| Code Walkthrough | Code blocks with explanation | 20 pts |
| Resource Compilation | 5+ curated links with descriptions | 15 pts |
| Community Newsletter | Weekly/monthly roundup posts | 25 pts |
| Translation | FAQ/guide translated to another language | 20 pts |

### Creator Spotlight Format

```
✍️ Content Creator Spotlight — March 2026

🏆 Top Creators:
1. @alice — 3 tutorials, 89 total reactions
   Latest: "Building a real-time dashboard with WebSockets"
2. @bob — 2 guides + 5 translations, 67 total reactions
   Latest: "Docker networking explained for beginners"
3. @carol — 1 mega-guide, 54 reactions
   Latest: "The complete guide to testing React components"

🌟 Rising Creator: @dave (first tutorial published this month!)

📊 Community Content Stats:
• 12 original pieces published this month
• 340 total reactions on community content
• Most popular: @alice's WebSocket tutorial (42 👍)
```

### Commands

```bash
# Post creator spotlight
message send --channel discord --to "channel:GENERAL_ID" --text "✍️ Content Creator Spotlight: ..."

# Award creator badge
# Assign Discord role or update member profile
```

### Guidelines

- Quality over quantity — a single great guide beats 10 low-effort posts
- Distinguish between original content and reshared links
- Monthly spotlight post to recognize creators
- "Creator" badge at 5+ original pieces with positive reception
- Cross-promote community content in daily digest

---

## 32. Feedback Collector

Aggregate, categorize, and prioritize community feedback including bug reports, feature requests, and suggestions.

### Workflow

1. Detect feedback signals: messages containing "bug", "feature request", "suggestion", "wishlist", "it would be nice if"
2. Categorize: bug report / feature request / improvement / complaint / praise
3. De-duplicate similar feedback
4. Generate periodic feedback reports for the team
5. Track feedback status: new → acknowledged → in-progress → resolved

### Feedback Report Format

```
📋 Community Feedback Report — Week of March 3-9

🐛 Bug Reports (7 new):
1. [Critical] Login fails after password reset — 5 reports (de-duped)
2. [Medium] Dark mode breaks on settings page — 2 reports
3. [Low] Typo in onboarding email — 1 report

✨ Feature Requests (12 new):
1. 🔥 GitHub integration (8 upvotes) — most requested!
2. 📱 Mobile app (6 upvotes)
3. 🔔 Custom notification settings (4 upvotes)
4. ... and 9 more

💡 Suggestions (3 new):
1. "Add code syntax highlighting to the editor"
2. "Allow thread-level muting"
3. "Weekly office hours with the team"

📊 Feedback Trends:
• Bug reports: ↓20% vs last week (good!)
• Feature requests: ↑15% (community is engaged)
• Top category: integrations (mentioned 14 times)

✅ Resolved This Week: 3 items
```

### Commands

```bash
# Generate feedback report
# LLM prompt: "Categorize and summarize these community messages as feedback..."

# Post report
message send --channel discord --to "channel:ADMIN_CHANNEL_ID" --text "📋 Feedback Report: ..."

# Acknowledge feedback publicly
message send --channel discord --to "channel:GENERAL_ID" --text "✅ We heard you! GitHub integration is now on our roadmap. Thanks @user1, @user2 for the suggestion!"
```

### Guidelines

- Auto-detect feedback from natural conversation — don't require special commands
- De-duplicate aggressively — cluster similar requests
- Public acknowledgment when feedback leads to action
- Never ignore critical bug reports — escalate immediately
- Track resolution rate as a community health metric

---

## 33. Community Calendar

Manage community events with RSVPs, reminders, and post-event recaps.

### Workflow

1. Admin creates event: "create event: Community Hackathon, March 22, 10am-6pm UTC"
2. Bot posts event with RSVP reactions
3. Send reminders: 1 week, 1 day, 1 hour before
4. During event: manage logistics (links, resources, updates)
5. After event: generate recap with attendance and highlights

### Event Format

**Announcement:**
```
📅 Upcoming Event

🎉 Community Hackathon
📆 March 22, 2026 | 10:00 AM - 6:00 PM UTC
📍 Online (#hackathon channel)
🎯 Theme: Build something useful for the community

📝 Details:
• Teams of 2-4 people
• Any tech stack welcome
• Prizes for top 3 projects
• Mentors available for help

React to RSVP:
✅ I'm in! | ❓ Maybe | 👀 Just watching

Currently signed up: 23 members
```

**Reminder:**
```
⏰ Reminder: Community Hackathon starts in 1 hour!

📍 Head to #hackathon
👥 32 participants registered
📋 Quick links: [Rules] [Team Board] [Submission Form]

Good luck everyone! 🚀
```

**Recap:**
```
📋 Event Recap — Community Hackathon

⏱️ Duration: 8 hours | 👥 Attendees: 28/32 (88% show rate)

🏆 Winners:
1. 🥇 Team Alpha — "Community Dashboard" (12 votes)
2. 🥈 Team Beta — "FAQ Search Engine" (9 votes)
3. 🥉 Team Gamma — "Onboarding Flow Wizard" (7 votes)

📊 Stats:
• 8 teams participated
• 12 projects submitted
• 156 messages in #hackathon during the event

💬 Highlights:
• @alice live-coded a full dashboard in 4 hours
• Team Beta's demo got a standing ovation (20 🎉 reactions)

Next event: TBD — suggest ideas in #events!
```

### Commands

```bash
# Post event
message send --channel discord --to "channel:EVENTS_ID" --text "📅 Event: ..."

# Send reminder
message send --channel discord --to "channel:GENERAL_ID" --text "⏰ Reminder: ..."

# Post recap
message send --channel discord --to "channel:EVENTS_ID" --text "📋 Recap: ..."
```

### Guidelines

- Support recurring events (weekly meetups, monthly hackathons)
- Send reminders at configurable intervals
- Track RSVP vs actual attendance for planning
- Archive past events for throwback posts (module 22)
- See [references/community-calendar.md](references/community-calendar.md) for event templates

---

## 34. Admin Shift Scheduler

Automated moderator rotation, workload tracking, and coverage planning.

### Workflow

1. Configure admin team and their availability/timezone
2. Auto-generate weekly shift schedule ensuring coverage
3. Track each admin's moderation workload (actions taken, time spent)
4. Alert when a shift is uncovered or an admin is overloaded

### Schedule Format

```
📋 Admin Schedule — Week of March 10-16

| Time (UTC) | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|------------|-----|-----|-----|-----|-----|-----|-----|
| 00-08      | @alice | @bob | @alice | @bob | @alice | @carol | @carol |
| 08-16      | @dave | @dave | @eve | @dave | @eve | @alice | @bob |
| 16-24      | @bob | @alice | @bob | @carol | @carol | @dave | @eve |

⚠️ Gap: Sunday 00-08 — no admin available. @carol, can you cover?

📊 Last Week Workload:
• @alice: 12 mod actions, 3h active
• @bob: 8 mod actions, 2.5h active
• @carol: 15 mod actions, 4h active (consider reducing load)
• @dave: 6 mod actions, 2h active
• @eve: 10 mod actions, 3h active
```

### Commands

```bash
# Post schedule
message send --channel discord --to "channel:ADMIN_CHANNEL_ID" --text "📋 Admin Schedule: ..."

# Alert for uncovered shift
message send --channel discord --to "channel:ADMIN_CHANNEL_ID" --text "⚠️ Shift gap detected: ..."

# Weekly workload report
message send --channel discord --to "channel:ADMIN_CHANNEL_ID" --text "📊 Admin Workload: ..."
```

### Configuration

```json
{
  "admins": [
    {"id": "USER_ID", "name": "alice", "timezone": "US/Pacific", "max_hours_week": 10},
    {"id": "USER_ID", "name": "bob", "timezone": "Europe/London", "max_hours_week": 8}
  ],
  "shift_duration_hours": 8,
  "min_coverage": 1,
  "schedule_post_day": "sunday"
}
```

### Guidelines

- Respect timezone preferences — don't schedule someone at 3am their time
- Balance workload — track cumulative hours and rotate fairly
- Allow shift swaps: "@alice swap Monday with @bob's Tuesday"
- Alert if coverage drops below minimum (default: 1 admin online)
- Monthly summary of admin contributions for recognition

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
    "multilingual_bridge": true,
    "long_thread_summary": true,
    "throwback_posts": true,
    "office_hours": true,
    "collaborative_projects": true,
    "churn_prediction": true,
    "social_graph": true,
    "smart_tags": true,
    "winback_campaigns": true,
    "content_recommendation": true,
    "community_wiki": true,
    "content_creator_incentives": true,
    "feedback_collector": true,
    "community_calendar": true,
    "admin_shift_scheduler": true
  },
  "digest_time": "09:00",
  "moderation_level": "medium",
  "sentiment_alert_threshold": 0.3,
  "thread_timeout_hours": 24,
  "leaderboard_day": "monday",
  "conversation_starter_silence_hours": 4,
  "health_report_day": "monday",
  "thread_summary_threshold": 50,
  "throwback_min_history_days": 90,
  "churn_inactive_days": 14,
  "winback_cooldown_days": 30,
  "wiki_update_frequency": "weekly",
  "feedback_report_day": "friday",
  "admin_shift_hours": 8,
  "calendar_reminder_intervals": [168, 24, 1],
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
