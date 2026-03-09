# Throwback Posts — Content Selection

## What Makes a Good Throwback

### Include
- Popular discussions (10+ replies)
- Community milestones (member count, launches, events)
- Highly-reacted messages (10+ reactions)
- Memorable moments (funny exchanges, breakthrough solutions)
- First appearances of now-active members ("@alice's first message!")

### Exclude
- Negative incidents (drama, bans, heated arguments)
- Deleted messages or content from members who left
- Private or sensitive information
- Moderation actions
- Spam or low-quality content

## Lookback Windows

| Period | Label | When to Use |
|--------|-------|-------------|
| 1 month ago | "Last Month" | Daily, if content exists |
| 3 months ago | "A Quarter Ago" | Weekly highlight |
| 6 months ago | "Half a Year Ago" | Monthly feature |
| 1 year ago | "On This Day" | Daily, highest priority |

## Scoring Content for Throwbacks

```
throwback_score = (reply_count * 2) + (reaction_count * 1.5) + (unique_participants * 3) + milestone_bonus
```

- `milestone_bonus`: +50 for member milestones, +30 for launches, +20 for events
- Minimum score threshold: 15 (skip if nothing qualifies)

## Posting Rules

- Max 1 per day
- Post at 09:00 UTC (before daily digest)
- Skip weekends if configured
- Don't repeat the same throwback within 6 months
- If no qualifying content exists for a date, skip silently
