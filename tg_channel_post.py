#!/usr/bin/env python3
"""
Telegram Auto-Poster for Live TV Channel
Posts match schedules and streaming links to Telegram channel.

Usage:
  python3 tg_channel_post.py --test            # Test post to verify
  python3 tg_channel_post.py --daily            # Daily match schedule
  python3 tg_channel_post.py --match "Liverpool vs Man Utd|20:00"  # Single match alert
"""

import os, sys, requests, json
from datetime import datetime, timedelta

# Config
CHANNEL_ID = None  # Will be set after channel creation
BOT_TOKEN = "8965462020:AAH5K0B6oFX0g8QBqBP3hyFqH6j8vNBh3UQ"  # @gegelala_bot
LIVETV_URL = "https://wrpbill27-commits.github.io/livetv/"
GO_URL = "https://wrpbill27-commits.github.io/livetv/go.html"

# Affiliate product rotation
AFFILIATE_PRODUCTS = [
    ("📱 พัดลมพกพา GOOJODOQ Type-C", "https://s.shopee.co.th/1VwSH0puTc"),
    ("🧴 Kirei Kirei โฟมล้างมือ 3 ถุง", "https://s.shopee.co.th/3g0wqzhf4t"),
    ("💊 โพรไบโอติกส์ Supurra", "https://s.shopee.co.th/qglTmsRpY"),
]

# Match schedule template (update daily or use API)
# Thai football schedule needs manual update or API integration
MATCHES_TEMPLATE = """
📺 **ตารางบอลวันนี้ {date}**

{favorites}

🔥 **ดูสดฟรี 👇**
{livetv_link}

🛒 **ของดีบอกต่อ:**
{affiliate}

📱 _ดูผ่านมือถือได้ ไม่มีโฆษณา_
"""

def send_message(text, parse_mode="Markdown"):
    """Send message to Telegram channel"""
    if not CHANNEL_ID:
        print("❌ CHANNEL_ID not set! Create channel and set CHANNEL_ID in script.")
        return False
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": False,  # Allow link previews
    }
    r = requests.post(url, json=payload, timeout=10)
    if r.status_code == 200:
        print(f"✅ Posted to channel")
        return True
    else:
        print(f"❌ Failed: {r.status_code} {r.text}")
        return False

def get_daily_matches():
    """Get today's notable matches — hardcoded for now, can be API-driven later"""
    today = datetime.now().strftime("%d/%m/%Y")
    
    # TODO: Replace with live API like football-data.org or thesportsdb.com
    # For now, generic template
    favorites = """⚽ **พรีเมียร์ลีก**: ดูได้ที่ True Premier 1-5
🇹🇭 **ไทยลีก**: ดูได้ที่ True Sport, PPTV
🌍 **ลีกอื่นๆ**: La Liga, Serie A, Bundesliga"""
    
    import random
    aff = random.choice(AFFILIATE_PRODUCTS)
    aff_text = f"[{aff[0]}]({aff[1]})"
    
    return MATCHES_TEMPLATE.format(
        date=today,
        favorites=favorites,
        livetv_link=f"[👉 ดูบอลสด คลิกที่นี่]({GO_URL})",
        affiliate=aff_text
    )

def post_daily_schedule():
    """Post daily match schedule to channel"""
    text = get_daily_matches()
    return send_message(text)

def post_match_alert(team_a, team_b, kickoff_time):
    """Post pre-match alert 30 min before kickoff"""
    text = f"""⚽ **กำลังจะเริ่ม!**

{team_a} 🆚 {team_b}
⏰ เริ่ม {kickoff_time}

👉 [ดูสดที่นี่]({GO_URL})

📺 179 ช่อง ดูฟรี ไม่มีโฆษณา"""
    return send_message(text)

def post_test():
    """Send a test message"""
    text = f"""🧪 **ทดสอบระบบ**

Live TV Auto-Post ทำงานปกติ ✅

👉 [ดูบอลสดฟรี 24 ชม.]({GO_URL})

_{datetime.now().strftime('%d/%m/%Y %H:%M')}_"""
    return send_message(text)

def main():
    global CHANNEL_ID
    
    # TODO: After user creates channel, set this to the channel ID
    # Channel ID can be found by: forward a message from channel to @getidsbot
    # Or check in the bot's update log when added as admin
    
    if "--test" in sys.argv:
        if not CHANNEL_ID:
            print("⚠️ CHANNEL_ID not set. To test:")
            print("1. Create a channel in Telegram app")
            print("2. Add @gegelala_bot as admin (with post permission)")
            print("3. Forward any message from channel to @getidsbot to get ID")
            print("4. Set CHANNEL_ID in this script")
            return
        post_test()
    elif "--daily" in sys.argv:
        post_daily_schedule()
    elif "--match" in sys.argv:
        # Parse: --match "Team A vs Team B|20:00"
        for a in sys.argv:
            if a.startswith("--match"):
                continue
            if "|" in a:
                match_info, ko_time = a.split("|")
                teams = match_info.split(" vs ")
                if len(teams) == 2:
                    post_match_alert(teams[0], teams[1], ko_time)
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
