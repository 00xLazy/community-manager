# Community Wiki Organization

## Category Schema

Wiki content is organized into auto-detected categories:

```
wiki/
├── getting-started/      # Installation, setup, first steps
├── architecture/         # Design patterns, system design
├── frontend/            # UI, React, CSS, browser topics
├── backend/             # APIs, databases, server topics
├── devops/              # CI/CD, Docker, deployment
├── tools/               # IDEs, CLI tools, productivity
├── best-practices/      # Code quality, testing, security
├── troubleshooting/     # Common errors and fixes
└── community/           # Events, projects, meta discussions
```

## Entry Format

Each wiki entry contains:

```json
{
  "id": "wiki-001",
  "title": "Setting up Docker for local development",
  "category": "devops",
  "content": "Summarized knowledge...",
  "sources": [
    {"type": "discussion", "id": "msg-123", "date": "2026-02-15", "author": "alice"},
    {"type": "faq", "id": "faq-045", "date": "2026-03-01"},
    {"type": "office_hours", "id": "oh-012", "date": "2026-03-06", "expert": "bob"}
  ],
  "contributors": ["alice", "bob", "carol"],
  "created": "2026-02-15",
  "updated": "2026-03-09",
  "views": 45,
  "helpful_votes": 12
}
```

## Auto-Update Rules

1. **New FAQ entry added** → Check if a matching wiki page exists → Append or create
2. **Office hours Q&A extracted** → Create wiki entry if topic is new
3. **Popular discussion concluded** → LLM summarizes key takeaways → Add to wiki
4. **Existing entry contradicted** → Flag for admin review, don't auto-update

## Quality Signals

| Signal | Action |
|--------|--------|
| Entry has 0 views in 30 days | Archive |
| Entry contradicts newer info | Flag for review |
| Entry has 5+ helpful votes | Promote to "Featured" |
| Entry sourced from 3+ discussions | Mark as "Well-established" |

## Search

Members can search the wiki via:
- Direct query: "wiki: Docker networking"
- Inline suggestion: bot suggests wiki links when relevant topics come up
- Browse: "show wiki categories"
