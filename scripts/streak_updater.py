#!/usr/bin/env python3
"""
Evergreen Streak Saver Engine
Handles user activity checking, weather telemetry fetching, developer tip selection,
log updates, live README progress bar rendering, and webhook notifications.
"""

import sys
import os
import json
import urllib.request
import urllib.error
import datetime
import random
import re

# Ensure stdout handles UTF-8 on all platforms (including Windows console)
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

TIPS = [
    "💡 **Git Tip**: Use `git commit --amend --no-edit` to quickly add staged changes to your last commit.",
    "💡 **Python Tip**: Use `dict.get(key, default)` to safely access dictionary values without raising KeyError.",
    "💡 **JS Tip**: Use `structuredClone(obj)` for deep object cloning in modern JavaScript.",
    "💡 **CLI Tip**: Use `ctrl + r` to reverse search terminal command history instantly.",
    "💡 **Clean Code**: Keep functions small and focused on doing a single task exceptionally well.",
    "💡 **Git Tip**: Use `git log --oneline --graph --all` to view a compact visual tree of all branches.",
    "💡 **Dev Productivity**: Automate repetitive tasks so you can focus on core logic."
]

def get_ist_now():
    tz_ist = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    return datetime.datetime.now(tz_ist)

def check_activity(username="Karnvendrasingh", token=None, event_name=None):
    if event_name == "workflow_dispatch":
        print("Manual workflow_dispatch trigger detected. Forcing backup execution.")
        return False

    now_ist = get_ist_now()
    today_ist_str = now_ist.strftime("%Y-%m-%d")
    today_utc_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    print(f"Checking user activity for IST date {today_ist_str} (UTC date {today_utc_str})...")

    headers = {
        "User-Agent": "Evergreen-Streak-Saver",
        "Accept": "application/vnd.github+json"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"https://api.github.com/users/{username}/events/public"
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            events = json.loads(res.read().decode('utf-8'))
            for event in events:
                if event.get("type") == "PushEvent":
                    created_at_raw = event.get("created_at", "")
                    if created_at_raw:
                        # Parse ISO 8601 UTC timestamp
                        dt_utc = datetime.datetime.fromisoformat(created_at_raw.replace("Z", "+00:00"))
                        dt_ist = dt_utc.astimezone(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
                        event_ist_date = dt_ist.strftime("%Y-%m-%d")
                        event_utc_date = dt_utc.strftime("%Y-%m-%d")

                        if event_ist_date == today_ist_str or event_utc_date == today_utc_str:
                            print(f"::notice::Natural commit detected today ({today_ist_str})! Event time: {dt_ist.strftime('%Y-%m-%d %H:%M:%S IST')}. Skipping automated commit.")
                            return True
    except Exception as e:
        print(f"Warning: Could not fetch GitHub public events ({e}). Proceeding with streak safety check.")

    print("No natural commit detected yet today. Proceeding with streak backup.")
    return False

def get_weather_telemetry():
    url = "https://api.open-meteo.com/v1/forecast?latitude=28.61&longitude=77.20&current_weather=true"
    req = urllib.request.Request(url, headers={"User-Agent": "Evergreen-Streak-Saver"})
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read().decode('utf-8'))
            cw = data.get("current_weather", {})
            temp = cw.get("temperature", 26)
            wcode = cw.get("weathercode", 0)

            if wcode in (0, 1):
                condition = "☀️ Clear"
            elif wcode in (2, 3):
                condition = "⛅ Partly Cloudy"
            elif wcode in (45, 48):
                condition = "🌫️ Foggy"
            elif wcode in (51, 53, 55, 61, 63, 65):
                condition = "🌧️ Rain"
            elif wcode in (80, 81, 82):
                condition = "🌦️ Showers"
            else:
                condition = "🌤️ Fair"

            return f"{condition} {temp}°C"
    except Exception as e:
        print(f"Warning: Weather telemetry API error ({e}). Using default weather string.")
        return "🌤️ Fair 26°C"

def update_files():
    now_ist = get_ist_now()
    timestamp_str = now_ist.strftime("%Y-%m-%d %H:%M:%S IST")
    date_only = now_ist.strftime("%Y-%m-%d")
    time_only = now_ist.strftime("%H:%M:%S IST")

    telemetry = get_weather_telemetry()
    tip = random.choice(TIPS)

    print(f"Timestamp: {timestamp_str}")
    print(f"Telemetry: {telemetry}")
    print(f"Selected Tip: {tip}")

    # 1. Update update.txt
    with open("update.txt", "w", encoding="utf-8") as f:
        f.write(f"Last updated: {timestamp_str}\n")

    # 2. Append to history.md
    history_line = f"| {date_only} {time_only} | Streak Safety Backup | {telemetry} | {tip} | ✅ Active |\n"
    with open("history.md", "a", encoding="utf-8") as f:
        f.write(history_line)

    # 3. Calculate backup count
    total_backups = 0
    if os.path.exists("history.md"):
        with open("history.md", "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("| 20"):
                    total_backups += 1
    if total_backups < 1:
        total_backups = 1

    # 4. Calculate Day of Year & Progress Bar
    year = now_ist.year
    is_leap = (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))
    total_days = 366 if is_leap else 365
    day_of_year = now_ist.timetuple().tm_yday
    percent = int(day_of_year * 100 / total_days)
    filled = int(percent / 5)
    empty = 20 - filled
    bar = "█" * filled + "░" * empty

    progress_line = f"🎯 **{year} Annual Goal**: [`{bar}`] **{day_of_year}/{total_days} Days** ({percent}%)"

    # 5. Update README.md
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()

        # Replace Annual Goal line
        content = re.sub(r"🎯 \*\*.* Annual Goal\*\*:.*", progress_line, content)

        # Replace Developer Tip line
        content = re.sub(r"> 💡 \*\*(Developer Tip of the Day|.*Tip.*)\*\*:.*", f"> {tip}", content)

        # Replace Saved Backups badge count
        content = re.sub(r"Saved%20Backups-\d+", f"Saved%20Backups-{total_backups}", content)

        with open("README.md", "w", encoding="utf-8") as f:
            f.write(content)

    print(f"Successfully updated update.txt, history.md, and README.md (Backups: {total_backups}).")
    return timestamp_str, telemetry, tip

def send_notifications(timestamp_str, telemetry, tip):
    discord_webhook = os.getenv("DISCORD_WEBHOOK", "").strip()
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()

    if discord_webhook:
        payload = {
            "embeds": [{
                "title": "🌱 Evergreen Streak Saved!",
                "color": 3066993,
                "fields": [
                    {"name": "Date & Time", "value": timestamp_str, "inline": True},
                    {"name": "Weather Telemetry", "value": telemetry, "inline": True},
                    {"name": "Developer Tip", "value": tip, "inline": False}
                ],
                "footer": {"text": "Evergreen Streak • Automating Productivity"}
            }]
        }
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(discord_webhook, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=10) as res:
                print("Discord notification sent successfully.")
        except Exception as e:
            print(f"Discord notification failed: {e}")

    if telegram_bot_token and telegram_chat_id:
        msg = f"🌱 *Evergreen Streak Saved!*\n\n📅 *Time:* {timestamp_str}\n🌤️ *Weather:* {telemetry}\n💡 *Tip:* _{tip}_"
        payload = {
            "chat_id": telegram_chat_id,
            "text": msg,
            "parse_mode": "Markdown"
        }
        data = json.dumps(payload).encode('utf-8')
        url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=10) as res:
                print("Telegram notification sent successfully.")
        except Exception as e:
            print(f"Telegram notification failed: {e}")

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--run-update"
    token = os.getenv("GITHUB_TOKEN", "").strip()
    event_name = os.getenv("GITHUB_EVENT_NAME", "").strip()

    if mode == "--check-activity":
        skip = check_activity(token=token, event_name=event_name)
        github_output = os.getenv("GITHUB_OUTPUT")
        if github_output and os.path.exists(github_output):
            with open(github_output, "a", encoding="utf-8") as f:
                f.write(f"skip={'true' if skip else 'false'}\n")
        sys.exit(0)

    elif mode == "--run-update":
        timestamp_str, telemetry, tip = update_files()
        send_notifications(timestamp_str, telemetry, tip)
        sys.exit(0)

if __name__ == "__main__":
    main()
