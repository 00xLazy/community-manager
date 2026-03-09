# Churn Prediction Methodology

## Risk Scoring

Each member gets a churn risk score (0-100) based on weighted signals:

```
churn_score = Σ(signal_value × signal_weight) / max_possible_score × 100
```

## Signals

### Activity Signals

| Signal | Weight | Calculation |
|--------|--------|-------------|
| Message frequency drop | 30 | (baseline - current) / baseline |
| Days since last message | 25 | min(days_inactive / 30, 1.0) |
| Reaction frequency drop | 10 | (baseline - current) / baseline |
| Channel diversity drop | 10 | (baseline_channels - current_channels) / baseline |

### Context Signals

| Signal | Weight | Calculation |
|--------|--------|-------------|
| Last interaction negative | 15 | 1.0 if last message had negative sentiment |
| Unanswered question | 10 | 1.0 if their last question got no reply |

## Baseline Calculation

- Baseline = average activity over the member's first 30 active days
- Update baseline monthly (rolling 90-day window)
- New members (< 14 days) are excluded from churn prediction

## Risk Levels

| Score | Level | Action |
|-------|-------|--------|
| 0-30 | Low | No action |
| 31-60 | Medium | Include in weekly report |
| 61-80 | High | Alert admin, suggest check-in |
| 81-100 | Critical | Immediate admin notification |

## Re-engagement Tracking

After a win-back attempt, track:
- Did they return within 7 days?
- Did they stay for 14+ days?
- Did their activity return to baseline?

Success rate by method:
- Personal DM from admin: ~35% return rate
- Personalized content digest: ~20% return rate
- Mention in relevant discussion: ~15% return rate
- Generic "we miss you": ~5% return rate (avoid)
