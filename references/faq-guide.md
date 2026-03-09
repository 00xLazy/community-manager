# FAQ Configuration Guide

## Knowledge Base Format

The FAQ knowledge base is a JSON file stored at `~/.openclaw/community/faq.json`.

### Structure

```json
{
  "faqs": [
    {
      "id": "install-guide",
      "patterns": ["how to install", "setup", "getting started"],
      "answer": "Follow our install guide: https://example.com/docs/install",
      "category": "setup",
      "language": "en"
    }
  ],
  "fallback": "I'm not sure about that. Let me flag this for a moderator.",
  "confidence_threshold": 0.7
}
```

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Unique identifier for the FAQ entry |
| `patterns` | yes | Array of trigger phrases (semantic matching, not exact) |
| `answer` | yes | The response to send |
| `category` | no | Group FAQs for reporting (e.g., "billing", "setup") |
| `language` | no | Primary language of this FAQ (default: community language) |

### Matching Rules

1. **Semantic match**: Use LLM to compare incoming question against patterns — not just keyword matching
2. **Confidence threshold**: Only auto-reply when confidence > `confidence_threshold` (default 0.7)
3. **Multi-match**: If multiple FAQs match, pick the highest confidence one
4. **No match**: Stay silent; optionally log the question to admin channel

### Adding New FAQs

When a question appears 3+ times without a match:

1. Log it to the admin channel as a suggestion
2. Format: "💡 Suggested FAQ: '{question}' was asked {count} times this week"
3. Admin can approve and add it to the knowledge base

### Multilingual FAQs

For multilingual communities, provide translations:

```json
{
  "id": "install-guide",
  "patterns": ["how to install", "如何安装", "cómo instalar"],
  "answer": {
    "en": "Follow our install guide: ...",
    "zh": "请参考安装指南: ...",
    "es": "Sigue nuestra guía de instalación: ..."
  }
}
```

When the answer is an object (keyed by language code), reply in the detected language. Fall back to `en` if the detected language is not available.
