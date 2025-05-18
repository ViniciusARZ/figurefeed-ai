import os
import requests
from uuid import uuid4

from google_photos_client.google_photos_client import (
    GooglePhotosClient,
    load_uploaded_ids,
    save_uploaded_id,
    upload_image_to_imgur,
    delete_from_imgur
)
from meta_client.instagram_client import post_image_to_instagram
from agents.get_caption import crew_get_caption

def post_latest_google_photo(album_id, openai_api_key, access_token, ig_user_id, imgur_client_id):
    print("Loading uploaded image IDs...")
    uploaded_ids = load_uploaded_ids()

    print("Connecting to Google Photos...")
    client = GooglePhotosClient()
    media_items = client.get_photos_from_album(album_id, page_size=20)
    print(f"Found {len(media_items)} media items in album.")

    for item in media_items:
        media_id = item["id"]
        if media_id in uploaded_ids:
            continue

        print(f"Found new image: {media_id}")
        image_url = item["baseUrl"] + "=w1080"
        print(f"Downloading image: {image_url}")
        image_res = requests.get(image_url)
        image_res.raise_for_status()

        print("Generating caption with AI...")
        caption = crew_get_caption(image_res.content, api_key=openai_api_key)
        if hasattr(caption, "result"):
            caption_text = caption.result
        else:
            caption_text = str(caption)
        # Append attribution text
        caption_text = f"{caption_text}\n\npowered by figurefeed-ai"

        if not caption_text.strip() or "answer" in caption_text.lower():
            raise ValueError("Invalid caption received.")
            
        print("Uploading to Imgur...")
        imgur_data = upload_image_to_imgur(image_res.content, imgur_client_id)

        print("Posting image to Instagram...")
        post_id = post_image_to_instagram(imgur_data['link'], caption_text, access_token, ig_user_id)
        print(f"Image posted to Instagram. Post ID: {post_id}")

        delete_from_imgur(imgur_data['deletehash'], imgur_client_id)
        save_uploaded_id(media_id)

        print("Workflow completed successfully.")
        return True

    print("No new images to post.")
    return False
