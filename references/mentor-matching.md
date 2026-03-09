# Mentor Matching Algorithm

## Matching Score

For each potential mentor-mentee pair, calculate:

```
match_score = (expertise_overlap * 0.4) + (availability * 0.2) + (helpfulness * 0.3) + (language_match * 0.1)
```

### Expertise Overlap (0-1)

Compare mentee's stated interests against mentor's demonstrated expertise:

```
overlap = |mentee_interests ∩ mentor_expertise| / |mentee_interests|
```

Expertise is derived from:
- Topics of questions they've answered
- Channels they're most active in
- Self-declared skills (if profile exists)

### Availability (0-1)

Based on mentor's current load:
- 0 mentees: 1.0
- 1 mentee: 0.8
- 2 mentees: 0.5
- 3 mentees: 0.0 (full)

### Helpfulness (0-1)

Normalized score based on:
- Answer acceptance rate (got "thanks" or positive reaction)
- Average response time to questions
- Consistency (active in the last 7 days)

### Language Match (0-1)

- Same primary language: 1.0
- Different but mentor knows mentee's language: 0.7
- English-only overlap: 0.5

## Matching Process

1. New member introduces themselves (keywords extracted by LLM)
2. Filter mentors: opted-in, < 3 mentees, active in last 7 days
3. Calculate match_score for each candidate
4. Present top 3 matches to mentee for selection
5. Notify selected mentor for acceptance

## Follow-Up Schedule

- Day 1: Introduction message
- Day 7: Check-in ("How's the mentorship going?")
- Day 30: Review ("Would you like to continue or be matched with someone new?")
- If no interaction for 14 days: gently close the pairing

## Opt-In Commands

- `!mentor on` — register as available mentor
- `!mentor off` — stop accepting new mentees
- `!mentor status` — view current mentees
- `!mentor areas [topics]` — set expertise areas
