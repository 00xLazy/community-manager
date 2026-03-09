#!/usr/bin/env python3
"""Generate a community health report from activity data.

Usage:
    python3 health_report.py --input activity.json [--period weekly|monthly]

Input format (activity.json):
    {
        "period": "2026-03-03 to 2026-03-09",
        "members": {
            "total": 420,
            "new": 23,
            "active": 156,
            "churned": 5
        },
        "messages": {
            "total": 2341,
            "by_channel": {"general": 534, "support": 312, "dev": 287}
        },
        "questions": {
            "asked": 89,
            "answered": 79,
            "avg_response_minutes": 12
        },
        "sentiment": {
            "overall": 0.72,
            "by_channel": {"general": 0.81, "support": 0.45, "showcase": 0.91}
        },
        "top_contributors": [
            {"user": "alice", "helpful_answers": 42},
            {"user": "bob", "helpful_answers": 38}
        ],
        "previous_period": {
            "members_new": 20,
            "messages_total": 2168,
            "questions_answer_rate": 0.87,
            "avg_response_minutes": 15,
            "sentiment_overall": 0.69,
            "health_score": 84
        }
    }

Output: A formatted health report to stdout.
"""

import argparse
import json
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Generate community health report")
    parser.add_argument("--input", required=True, help="Path to activity JSON file")
    parser.add_argument("--period", default="weekly", choices=["weekly", "monthly"])
    parser.add_argument("--format", default="markdown", choices=["markdown", "json"])
    return parser.parse_args()


def trend(current, previous):
    """Return trend arrow and percentage."""
    if previous == 0:
        return "new"
    diff = ((current - previous) / previous) * 100
    if diff > 0:
        return f"↑{diff:.0f}%"
    elif diff < 0:
        return f"↓{abs(diff):.0f}%"
    return "→ flat"


def calculate_health_score(data):
    """Calculate overall health score (0-100)."""
    scores = []

    # Engagement (0-25)
    members = data.get("members", {})
    active_ratio = members.get("active", 0) / max(members.get("total", 1), 1)
    scores.append(min(active_ratio * 100, 25))

    # Response quality (0-25)
    questions = data.get("questions", {})
    asked = questions.get("asked", 0)
    if asked > 0:
        answer_rate = questions.get("answered", 0) / asked
        scores.append(min(answer_rate * 25, 25))
    else:
        scores.append(20)

    # Sentiment (0-25)
    sentiment = data.get("sentiment", {}).get("overall", 0.5)
    scores.append(min(max(sentiment, 0) * 25, 25))

    # Growth (0-25)
    new_members = members.get("new", 0)
    churned = members.get("churned", 0)
    net_growth = new_members - churned
    growth_score = min(max(net_growth / max(new_members, 1), 0) * 25, 25)
    scores.append(growth_score)

    return round(sum(scores))


def format_markdown(data, period):
    """Format health report as markdown."""
    members = data.get("members", {})
    messages = data.get("messages", {})
    questions = data.get("questions", {})
    sentiment = data.get("sentiment", {})
    top = data.get("top_contributors", [])
    prev = data.get("previous_period", {})

    health_score = calculate_health_score(data)
    prev_score = prev.get("health_score", health_score)
    score_trend = trend(health_score, prev_score)

    period_str = data.get("period", "this period")

    lines = [
        f"📊 Community Health Report — {period_str}",
        "",
        f"🌡️ Overall Health Score: {health_score}/100 ({score_trend} from last {period})",
        "",
        "📈 Growth:",
        f"• New members: {members.get('new', 0)} ({trend(members.get('new', 0), prev.get('members_new', 0))})",
        f"• Member retention: {100 - round(members.get('churned', 0) / max(members.get('total', 1), 1) * 100)}%",
        f"• Active members: {members.get('active', 0)}/{members.get('total', 0)} ({round(members.get('active', 0) / max(members.get('total', 1), 1) * 100)}%)",
        "",
        "💬 Engagement:",
        f"• Messages: {messages.get('total', 0)} ({trend(messages.get('total', 0), prev.get('messages_total', 0))})",
        f"• Avg response time: {questions.get('avg_response_minutes', 0)} min ({trend(questions.get('avg_response_minutes', 0), prev.get('avg_response_minutes', 0))})",
    ]

    asked = questions.get("asked", 0)
    answered = questions.get("answered", 0)
    if asked > 0:
        answer_rate = round(answered / asked * 100)
        prev_rate = round(prev.get("questions_answer_rate", 0) * 100)
        lines.append(f"• Questions answered: {answer_rate}% ({trend(answer_rate, prev_rate)})")

    by_channel = messages.get("by_channel", {})
    if by_channel:
        most_active = max(by_channel, key=by_channel.get)
        quietest = min(by_channel, key=by_channel.get)
        lines.append(f"• Most active channel: #{most_active} ({by_channel[most_active]} msgs)")
        lines.append(f"• Quietest channel: #{quietest} ({by_channel[quietest]} msgs)")

    lines.append("")
    lines.append("😊 Sentiment:")
    lines.append(f"• Overall: {sentiment.get('overall', 0):.2f} ({'positive' if sentiment.get('overall', 0) > 0.6 else 'neutral' if sentiment.get('overall', 0) > 0.3 else 'negative'})")

    sent_by_ch = sentiment.get("by_channel", {})
    if sent_by_ch:
        happiest = max(sent_by_ch, key=sent_by_ch.get)
        saddest = min(sent_by_ch, key=sent_by_ch.get)
        lines.append(f"• Happiest channel: #{happiest} ({sent_by_ch[happiest]:.2f})")
        if sent_by_ch[saddest] < 0.5:
            lines.append(f"• Needs attention: #{saddest} ({sent_by_ch[saddest]:.2f})")

    if top:
        lines.append("")
        lines.append("🏆 Top Contributors:")
        for c in top[:3]:
            lines.append(f"• @{c['user']} ({c['helpful_answers']} helpful answers)")

    # AI-generated action items
    lines.append("")
    lines.append("⚠️ Action Items:")
    if sent_by_ch:
        for ch, score in sent_by_ch.items():
            if score < 0.5:
                lines.append(f"• #{ch} sentiment is low ({score:.2f}) — consider adding more support")
    if asked > 0 and (asked - answered) > 5:
        lines.append(f"• {asked - answered} questions went unanswered — review thread tracker")
    if by_channel:
        for ch, count in by_channel.items():
            if count < 20:
                lines.append(f"• #{ch} has low engagement ({count} msgs) — try a discussion starter")

    if not any(line.startswith("•") for line in lines[lines.index("⚠️ Action Items:") + 1:]):
        lines.append("• No urgent action items — community is healthy! 🎉")

    return "\n".join(lines)


def main():
    args = parse_args()

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    if args.format == "markdown":
        print(format_markdown(data, args.period))
    else:
        data["health_score"] = calculate_health_score(data)
        print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
