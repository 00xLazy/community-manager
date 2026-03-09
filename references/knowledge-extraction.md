# Knowledge Extraction Heuristics

## Detection Signals

A message pair (question + answer) is a knowledge extraction candidate when:

### Strong Signals (any one triggers extraction)
- Admin/mod reacts with 📌 or uses `!save` command
- Answer gets 3+ positive reactions (thumbs up, heart, star)
- Asker replies with "thanks", "that worked", "perfect", "solved"

### Medium Signals (need 2+ to trigger)
- Answer is >50 words (substantive)
- Answer contains a code block or link
- Answer is from a recognized helper (high engagement score)
- Multiple users react positively

### Weak Signals (context only, don't trigger alone)
- Answer is a reply to a message ending with "?"
- Answer author has helper role
- Thread has been marked as resolved

## De-duplication

Before adding to the knowledge base:

1. Extract key terms from the question
2. Compare against existing FAQ patterns using semantic similarity
3. If similarity > 0.85: flag as potential duplicate, ask admin to merge or skip
4. If similarity 0.6-0.85: suggest as a related FAQ variant
5. If similarity < 0.6: add as new entry

## Extraction Pipeline

```
Message detected → Signal scoring → Threshold check → Q&A pair extraction
→ De-duplication check → Format as FAQ entry → Submit for admin review
```

## Review Notification

```
📚 New Knowledge Captured

Q: "How do I reset my API key?"
A: "Go to Settings > API > Regenerate. Your old key is invalidated immediately."

Source: @helpful_user in #support (Mar 9)
Confidence: 0.92 (strong signal: 5 reactions + "thanks" reply)

React ✅ to approve, ❌ to discard, ✏️ to edit before adding.
```
