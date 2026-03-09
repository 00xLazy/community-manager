#!/usr/bin/env python3
"""Detect anomalous community events from a stream of events.

Usage:
    python3 event_detector.py --input events.json [--thresholds thresholds.json]

Input format (events.json):
    [
        {
            "type": "join|leave|message|reaction",
            "user": "username",
            "timestamp": "2026-03-09T12:34:56Z",
            "channel": "general",
            "content": "optional message content",
            "account_age_hours": 2
        }
    ]

Output: Detected events as JSON to stdout.
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta


DEFAULT_THRESHOLDS = {
    "raid_joins_count": 10,
    "raid_window_minutes": 5,
    "spam_identical_count": 5,
    "spam_window_minutes": 5,
    "keyword_spike_count": 15,
    "keyword_spike_window_minutes": 10,
    "mass_leave_count": 10,
    "mass_leave_window_minutes": 60,
    "link_flood_count": 10,
    "link_flood_window_minutes": 5,
    "new_account_threshold_hours": 24,
}


def parse_args():
    parser = argparse.ArgumentParser(description="Detect anomalous community events")
    parser.add_argument("--input", required=True, help="Path to events JSON file")
    parser.add_argument("--thresholds", help="Path to thresholds JSON file (optional)")
    return parser.parse_args()


def parse_ts(ts_str):
    """Parse ISO timestamp string to datetime."""
    return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))


def detect_raid(events, thresholds):
    """Detect mass join events from new accounts."""
    joins = [e for e in events if e.get("type") == "join"]
    if len(joins) < thresholds["raid_joins_count"]:
        return None

    window = timedelta(minutes=thresholds["raid_window_minutes"])
    joins_sorted = sorted(joins, key=lambda e: parse_ts(e["timestamp"]))

    for i in range(len(joins_sorted)):
        t_start = parse_ts(joins_sorted[i]["timestamp"])
        t_end = t_start + window
        window_joins = [
            j for j in joins_sorted[i:]
            if parse_ts(j["timestamp"]) <= t_end
        ]
        if len(window_joins) >= thresholds["raid_joins_count"]:
            new_accounts = [
                j for j in window_joins
                if j.get("account_age_hours", 9999) < thresholds["new_account_threshold_hours"]
            ]
            return {
                "event": "raid_detected",
                "severity": "high",
                "details": {
                    "joins_in_window": len(window_joins),
                    "new_accounts": len(new_accounts),
                    "window_start": joins_sorted[i]["timestamp"],
                    "users": [j["user"] for j in window_joins[:20]],
                },
            }
    return None


def detect_spam_wave(events, thresholds):
    """Detect identical messages from different users."""
    messages = [e for e in events if e.get("type") == "message" and e.get("content")]
    content_users = defaultdict(set)

    for msg in messages:
        content_users[msg["content"]].add(msg["user"])

    for content, users in content_users.items():
        if len(users) >= thresholds["spam_identical_count"]:
            return {
                "event": "spam_wave_detected",
                "severity": "high",
                "details": {
                    "identical_message": content[:100],
                    "unique_senders": len(users),
                    "senders": list(users)[:10],
                },
            }
    return None


def detect_mass_leave(events, thresholds):
    """Detect mass member departure."""
    leaves = [e for e in events if e.get("type") == "leave"]
    if len(leaves) < thresholds["mass_leave_count"]:
        return None

    window = timedelta(minutes=thresholds["mass_leave_window_minutes"])
    leaves_sorted = sorted(leaves, key=lambda e: parse_ts(e["timestamp"]))

    for i in range(len(leaves_sorted)):
        t_start = parse_ts(leaves_sorted[i]["timestamp"])
        t_end = t_start + window
        window_leaves = [
            l for l in leaves_sorted[i:]
            if parse_ts(l["timestamp"]) <= t_end
        ]
        if len(window_leaves) >= thresholds["mass_leave_count"]:
            return {
                "event": "mass_leave_detected",
                "severity": "medium",
                "details": {
                    "leaves_in_window": len(window_leaves),
                    "window_start": leaves_sorted[i]["timestamp"],
                    "users": [l["user"] for l in window_leaves[:20]],
                },
            }
    return None


def detect_link_flood(events, thresholds):
    """Detect mass link posting from new accounts."""
    messages = [e for e in events if e.get("type") == "message" and e.get("content")]
    link_msgs = [
        m for m in messages
        if ("http://" in m.get("content", "") or "https://" in m.get("content", ""))
        and m.get("account_age_hours", 9999) < thresholds["new_account_threshold_hours"]
    ]

    if len(link_msgs) < thresholds["link_flood_count"]:
        return None

    window = timedelta(minutes=thresholds["link_flood_window_minutes"])
    link_msgs_sorted = sorted(link_msgs, key=lambda e: parse_ts(e["timestamp"]))

    for i in range(len(link_msgs_sorted)):
        t_start = parse_ts(link_msgs_sorted[i]["timestamp"])
        t_end = t_start + window
        window_msgs = [
            m for m in link_msgs_sorted[i:]
            if parse_ts(m["timestamp"]) <= t_end
        ]
        if len(window_msgs) >= thresholds["link_flood_count"]:
            return {
                "event": "link_flood_detected",
                "severity": "high",
                "details": {
                    "links_in_window": len(window_msgs),
                    "window_start": link_msgs_sorted[i]["timestamp"],
                    "senders": list(set(m["user"] for m in window_msgs))[:10],
                },
            }
    return None


def main():
    args = parse_args()

    with open(args.input, encoding="utf-8") as f:
        events = json.load(f)

    thresholds = dict(DEFAULT_THRESHOLDS)
    if args.thresholds:
        with open(args.thresholds, encoding="utf-8") as f:
            thresholds.update(json.load(f))

    detectors = [detect_raid, detect_spam_wave, detect_mass_leave, detect_link_flood]
    alerts = []

    for detector in detectors:
        result = detector(events, thresholds)
        if result:
            alerts.append(result)

    if alerts:
        print(json.dumps(alerts, indent=2, ensure_ascii=False))
    else:
        print(json.dumps({"status": "ok", "message": "No anomalies detected"}, indent=2))


if __name__ == "__main__":
    main()
