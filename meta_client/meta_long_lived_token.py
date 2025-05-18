import requests
import json

def get_long_lived_token():
    with open("meta_info.json", "r") as f:
        config = json.load(f)

    short_token = config["short_lived_token"]
    app_id = config["app_id"]
    app_secret = config["app_secret"]

    url = (
        "https://graph.facebook.com/v19.0/oauth/access_token"
        f"?grant_type=fb_exchange_token"
        f"&client_id={app_id}"
        f"&client_secret={app_secret}"
        f"&fb_exchange_token={short_token}"
    )

    print("🔄 Requesting long-lived token...")
    res = requests.get(url)
    data = res.json()

    if "access_token" in data:
        long_token = data["access_token"]
        print("✅ Long-lived token obtained.")
        print(f"\n🔐 TOKEN:\n{long_token}\n")
        return long_token
    else:
        print("❌ Failed to get long-lived token:", data)
        return None

if __name__ == "__main__":
    get_long_lived_token()
