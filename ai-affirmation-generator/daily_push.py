import os
import requests
import schedule
import time

# Load OneSignal credentials from environment variables
ONESIGNAL_APP_ID = os.getenv("ONESIGNAL_APP_ID")
ONESIGNAL_API_KEY = os.getenv("ONESIGNAL_API_KEY")

HEADERS = {
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": f"Basic {ONESIGNAL_API_KEY}"
}

def send_affirmation_push():
    affirmation = "💫 You are glowing gently, even in stillness."

    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "included_segments": ["Subscribed Users"],
        "headings": {"en": "Daily Affirmation"},
        "contents": {"en": affirmation},
        "url": "https://affirmations-generator.onrender.com"  # Optional
    }

    response = requests.post(
        "https://onesignal.com/api/v1/notifications",
        headers=HEADERS,
        json=payload
    )

    print("✅ Push sent:", response.json())

# Schedule to send once a day (e.g., 10:00 AM)
schedule.every().day.at("10:00").do(send_affirmation_push)

print("🔔 Daily Affirmation Push Scheduler is running...")

while True:
    schedule.run_pending()
    time.sleep(60)
