# Sentiment Tracking Methodology

## Scoring

Each message receives a sentiment score from the LLM:
- **+1**: Positive (praise, gratitude, excitement, agreement)
- **0**: Neutral (questions, factual statements, casual chat)
- **-1**: Negative (complaints, frustration, anger, disappointment)

## Rolling Score Calculation

Channel sentiment = (sum of scores in window) / (number of messages in window)

Result ranges from -1.0 (all negative) to +1.0 (all positive).

### Time Windows

- **1h window**: for real-time alerts (sharp mood swings)
- **24h window**: for daily digest sentiment section
- **7d window**: for weekly trend reporting

## Alert Thresholds

| Level | Condition | Action |
|-------|-----------|--------|
| Watch | 1h score < -0.2 | Log internally |
| Warning | 1h score < -0.3 | Alert admin channel |
| Critical | 1h score < -0.5 AND 10+ messages | Urgent alert with recommended response |

## Context Analysis

When alerting, include:
1. The top 3 negative keywords/themes (extracted by LLM)
2. Likely root cause if detectable (e.g., "users mentioning v2.1 update")
3. Suggested response template for admin

## Baseline Calibration

Different channels have different baselines:
- #support: naturally more negative (people come with problems)
- #general: should be mostly neutral/positive
- #feedback: mixed

Adjust thresholds per channel. Alert only on deviations from the channel's baseline, not absolute values.

## LLM Prompt Template

```
Analyze the sentiment of each message below. For each, respond with:
- sentiment: positive | neutral | negative
- confidence: 0.0-1.0

Then provide an overall summary with:
- overall_score: -1.0 to 1.0
- top_themes: list of 3 key themes
- mood_shift: improving | stable | declining

Messages:
{messages}
```
