#!/usr/bin/env python3
"""Generate a community digest from a JSON array of messages.

Usage:
    python3 digest.py --input messages.json [--format markdown|json] [--max-topics 5]

Input format (messages.json):
    [
        {
            "author": "username",
            "content": "message text",
            "timestamp": "2026-03-09T12:34:56Z",
            "channel": "general",
            "has_link": false,
            "is_question": false
        }
    ]

Output: A formatted digest string to stdout.
"""

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from urllib.parse import urlparse


def parse_args():
    parser = argparse.ArgumentParser(description="Generate community digest")
    parser.add_argument("--input", required=True, help="Path to messages JSON file")
    parser.add_argument("--format", default="markdown", choices=["markdown", "json"])
    parser.add_argument("--max-topics", type=int, default=5)
    return parser.parse_args()


def extract_links(text: str) -> list:
    """Extract URLs from message text."""
    words = text.split()
    return [w for w in words if w.startswith("http://") or w.startswith("https://")]


def is_question(text: str) -> bool:
    """Heuristic: does this message look like a question?"""
    stripped = text.strip()
    if stripped.endswith("?"):
        return True
    lower = stripped.lower()
    return any(lower.startswith(w) for w in ["how ", "what ", "why ", "where ", "when ", "who ", "is ", "can ", "does "])


def generate_digest(messages, max_topics: int = 5) -> dict:
    """Analyze messages and produce digest data."""
    if not messages:
        return {"empty": True, "date": datetime.now(timezone.utc).strftime("%Y-%m-%d")}

    authors = set()
    channels = Counter()
    questions = []
    links = []
    channel_messages = {}

    for msg in messages:
        author = msg.get("author", "unknown")
        content = msg.get("content", "")
        channel = msg.get("channel", "general")

        authors.add(author)
        channels[channel] += 1
        channel_messages.setdefault(channel, []).append(content)

        if is_question(content):
            questions.append({"question": content, "author": author})

        for link in extract_links(content):
            links.append({"url": link, "author": author})

    # Top channels by activity = "hot topics"
    hot_topics = channels.most_common(max_topics)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    return {
        "empty": False,
        "date": today,
        "total_messages": len(messages),
        "active_members": len(authors),
        "hot_topics": [{"channel": ch, "count": ct} for ch, ct in hot_topics],
        "unanswered_questions": questions[:10],
        "shared_links": links[:10],
    }


def format_markdown(digest: dict) -> str:
    """Format digest data as markdown."""
    if digest.get("empty"):
        return f"📋 Daily Digest — {digest['date']}\n\n😴 Quiet day — no significant activity."

    lines = [f"📋 Daily Digest — {digest['date']}", ""]

    # Hot topics
    lines.append("🔥 Hot Topics:")
    for topic in digest["hot_topics"]:
        lines.append(f"• #{topic['channel']}: {topic['count']} messages")
    lines.append("")

    # Unanswered questions
    if digest["unanswered_questions"]:
        lines.append("❓ Unanswered Questions:")
        for q in digest["unanswered_questions"][:5]:
            text = q["question"][:80] + ("..." if len(q["question"]) > 80 else "")
            lines.append(f'• "{text}" — @{q["author"]}')
        lines.append("")

    # Stats
    lines.append("📊 Activity:")
    lines.append(f"• Messages: {digest['total_messages']} | Active members: {digest['active_members']}")
    lines.append("")

    # Links
    if digest["shared_links"]:
        lines.append("🔗 Shared Links:")
        for link in digest["shared_links"][:5]:
            lines.append(f"• {link['url']}")
        lines.append("")

    return "\n".join(lines)


def format_json(digest: dict) -> str:
    """Format digest data as JSON."""
    return json.dumps(digest, indent=2, ensure_ascii=False)


def main():
    args = parse_args()

    with open(args.input, encoding="utf-8") as f:
        messages = json.load(f)

    digest = generate_digest(messages, max_topics=args.max_topics)

    if args.format == "markdown":
        print(format_markdown(digest))
    else:
        print(format_json(digest))


if __name__ == "__main__":
    main()
