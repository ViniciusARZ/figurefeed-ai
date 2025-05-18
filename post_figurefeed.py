import json
from workflow import post_latest_google_photo

if __name__ == "__main__":
    with open('config.json') as f:
        config = json.load(f)

    success = post_latest_google_photo(
        album_id=config['google_photos_album_id'],
        openai_api_key=config['openai_api_key'],
        access_token=config['meta_access_token'],
        ig_user_id=config['meta_ig_account_id'],
        imgur_client_id=config['imgur_client_id']
    )

    if success:
        print("Workflow completed successfully.")
    else:
        print("No new content to post.")
