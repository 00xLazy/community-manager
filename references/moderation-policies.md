# Moderation Policies

## Severity Levels

### Low — Monitor Only
- Off-topic messages in a focused channel
- Minor language issues
- Borderline self-promotion

**Action**: Log to admin channel. No public action.

### Medium — Warn
- Repeated off-topic posting
- Mild harassment or disrespectful language
- Unsolicited advertising

**Action**: Reply with a public warning. Notify admin channel.

Warning template:
```
⚠️ @{user}, your message appears to violate our community guidelines
regarding {category}. Please review our rules in #rules.
This is an automated warning.
```

### High — Remove
- Spam (repeated identical messages, bot-like behavior)
- Hate speech, slurs, or threats
- Phishing links or malware
- NSFW content in SFW channels
- Doxxing or sharing personal information

**Action**: Delete message immediately. Warn user. Log full details to admin channel.

## Detection Patterns

### Spam Indicators
- Same message posted 3+ times within 5 minutes
- Message contains 5+ links
- New account (joined < 24h ago) posting links
- Message matches known spam patterns

### Phishing Indicators
- URLs with misspelled domain names (e.g., "discrod.gift")
- "Free nitro" or similar social engineering phrases
- URL shorteners pointing to login pages

### Advertising
- Promotional language with external links
- "DM me for..." followed by commercial offers
- Crypto/NFT promotion in non-crypto communities

## Escalation Rules

1. First violation (medium): public warning
2. Second violation (medium) within 24h: mute for 1 hour (if platform supports)
3. Third violation or any high severity: notify admin for manual ban decision

## Important Safeguards

- **Never auto-ban** — always escalate to human admins
- **Never moderate admins/mods** — check role before acting
- **Log everything** — keep original message content for admin review
- **False positive recovery** — if a user disputes, immediately stop and flag for human review
- **Rate limit moderation** — max 10 auto-moderations per minute to prevent cascading errors
