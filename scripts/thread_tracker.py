#!/usr/bin/env python3
"""Track unanswered questions and stale threads.

Usage:
    python3 thread_tracker.py --input messages.json [--timeout 24]

Input format (messages.json):
    [
        {
            "id": "msg_001",
            "author": "username",
            "content": "message text",
            "timestamp": "2026-03-09T12:34:56Z",
            "channel": "support",
            "reply_to": null,
            "reactions": {"thumbsup": 2, "heart": 0}
        }
    ]

Output: A report of unanswered questions to stdout.
"""

import argparse
import json
import sys
from datetime import datetime, timezone, timedelta


def parse_args():
    parser = argparse.ArgumentParser(description="Track unanswered questions")
    parser.add_argument("--input", required=True, help="Path to messages JSON file")
    parser.add_argument("--timeout", type=int, default=24, help="Hours before a question is overdue")
    parser.add_argument("--format", default="markdown", choices=["markdown", "json"])
    return parser.parse_args()


def parse_ts(ts_str):
    return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))


def is_question(text):
    stripped = text.strip()
    if stripped.endswith("?"):
        return True
    lower = stripped.lower()
    return any(lower.startswith(w) for w in [
        "how ", "what ", "why ", "where ", "when ", "who ",
        "is ", "can ", "does ", "could ", "would ", "should ",
    ])


def is_thanks(text):
    lower = text.strip().lower()
    thanks_phrases = ["thanks", "thank you", "thx", "that worked", "perfect", "solved", "got it"]
    return any(phrase in lower for phrase in thanks_phrases)


def find_unanswered(messages, timeout_hours):
    now = datetime.now(timezone.utc)
    timeout = timedelta(hours=timeout_hours)

    questions = {}
    for msg in messages:
        if is_question(msg.get("content", "")):
            questions[msg["id"]] = {
                "id": msg["id"],
                "question": msg["content"],
                "author": msg["author"],
                "channel": msg.get("channel", "unknown"),
                "timestamp": msg["timestamp"],
                "answered": False,
            }

    for msg in messages:
        reply_to = msg.get("reply_to")
        if reply_to and reply_to in questions:
            content = msg.get("content", "")
            reactions = msg.get("reactions", {})
            has_substance = len(content.split()) > 3
            has_positive_reaction = sum(reactions.values()) > 0

            if has_substance or has_positive_reaction:
                questions[reply_to]["answered"] = True

        if is_thanks(msg.get("content", "")) and reply_to and reply_to in questions:
            questions[reply_to]["answered"] = True

    unanswered = []
    for q in questions.values():
        if q["answered"]:
            continue
        q_time = parse_ts(q["timestamp"])
        age = now - q_time
        age_hours = age.total_seconds() / 3600
        q["age_hours"] = round(age_hours, 1)
        q["overdue"] = age_hours > timeout_hours
        unanswered.append(q)

    unanswered.sort(key=lambda x: x["age_hours"], reverse=True)
    return unanswered


def format_markdown(unanswered, timeout_hours):
    if not unanswered:
        return "✅ No unanswered questions — all caught up!"

    overdue = [q for q in unanswered if q["overdue"]]
    approaching = [q for q in unanswered if not q["overdue"] and q["age_hours"] > timeout_hours / 2]
    recent = [q for q in unanswered if not q["overdue"] and q["age_hours"] <= timeout_hours / 2]

    lines = ["📋 Unanswered Questions Report", ""]

    if overdue:
        lines.append(f"⏰ Overdue (>{timeout_hours}h):")
        for q in overdue[:10]:
            text = q["question"][:60] + ("..." if len(q["question"]) > 60 else "")
            lines.append(f'• "{text}" — @{q["author"]} in #{q["channel"]} ({q["age_hours"]}h ago)')
        lines.append("")

    if approaching:
        lines.append(f"⚠️ Approaching deadline (>{timeout_hours // 2}h):")
        for q in approaching[:10]:
            text = q["question"][:60] + ("..." if len(q["question"]) > 60 else "")
            lines.append(f'• "{text}" — @{q["author"]} in #{q["channel"]} ({q["age_hours"]}h ago)')
        lines.append("")

    if recent:
        lines.append(f"🕐 Recent (<{timeout_hours // 2}h):")
        for q in recent[:5]:
            text = q["question"][:60] + ("..." if len(q["question"]) > 60 else "")
            lines.append(f'• "{text}" — @{q["author"]} in #{q["channel"]} ({q["age_hours"]}h ago)')
        lines.append("")

    lines.append(f"Total unanswered: {len(unanswered)}")
    return "\n".join(lines)


def main():
    args = parse_args()

    with open(args.input, encoding="utf-8") as f:
        messages = json.load(f)

    unanswered = find_unanswered(messages, args.timeout)

    if args.format == "markdown":
        print(format_markdown(unanswered, args.timeout))
    else:
        print(json.dumps(unanswered, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
