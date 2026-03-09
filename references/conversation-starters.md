# Conversation Starter Templates

## Topic Categories

### This or That
- "Tabs or spaces? And why?"
- "Monorepo or polyrepo?"
- "REST or GraphQL for a new project in 2026?"
- "TypeScript or plain JavaScript?"
- "Docker or native dev environment?"

### Show & Tell
- "What's the coolest thing you built this week?"
- "Share a tool that changed your workflow recently"
- "Show us your terminal/IDE setup"
- "What open source project are you contributing to?"

### Hypothetical
- "If you could mass-delete one technology, what would it be?"
- "You have unlimited budget for one dev tool. What do you build?"
- "If you had to start a startup today, what would you build?"

### Retrospective
- "What's the best thing you learned this week?"
- "What's a mistake you made recently that taught you something?"
- "What habit improved your productivity the most?"

### Community-Specific
Generate based on recent trending topics. LLM prompt:

```
Based on these recent community discussions:
{recent_topics}

Generate 1 engaging discussion question that:
- Is related to a topic the community cares about
- Is open-ended (no single right answer)
- Encourages sharing personal experience
- Is concise (under 30 words)
```

## Timing Rules

- Post only after {silence_hours}h of inactivity (default: 4h)
- Never post between 22:00-08:00 in the community's timezone
- Max 1 starter per channel per day
- Skip weekends if configured
- Don't post if there's an active AMA or event

## Engagement Tracking

If a topic gets:
- 0-2 replies: topic type was a miss, rotate to a different category
- 3-10 replies: moderate success, reuse this category occasionally
- 10+ replies: great topic, analyze what made it work and generate similar ones
