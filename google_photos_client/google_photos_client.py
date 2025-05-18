from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import requests
import os
import json
import base64

SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']
API_BASE_URL = 'https://photoslibrary.googleapis.com/v1'

IMGUR_UPLOAD_URL = "https://api.imgur.com/3/image"
IMGUR_DELETE_URL = "https://api.imgur.com/3/image/{deletehash}"

IMAGES_UPLOADED_FILE = "images_uploaded.json"

class GooglePhotosClient:
    def __init__(self, credentials_path='google_credentials.json', token_path='token.json'):
        self.creds = None
        if token_path:
            try:
                self.creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            except Exception:
                pass
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(self.creds.to_json())

    def list_albums(self):
        res = requests.get(f"{API_BASE_URL}/albums", headers={"Authorization": f"Bearer {self.creds.token}"})
        return res.json().get('albums', [])

    def get_photos_from_album(self, album_id, page_size=10):
        url = f"{API_BASE_URL}/mediaItems:search"
        headers = {"Authorization": f"Bearer {self.creds.token}"}
        payload = {"albumId": album_id, "pageSize": page_size}
        res = requests.post(url, headers=headers, json=payload)
        return res.json().get('mediaItems', [])


def load_uploaded_ids():
    if os.path.exists(IMAGES_UPLOADED_FILE):
        with open(IMAGES_UPLOADED_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_uploaded_id(media_id):
    uploaded = load_uploaded_ids()
    uploaded.add(media_id)
    with open(IMAGES_UPLOADED_FILE, "w") as f:
        json.dump(list(uploaded), f)


def upload_image_to_imgur(image_bytes, imgur_client_id):
    print("☁️ Uploading image to Imgur...")
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    res = requests.post(
        IMGUR_UPLOAD_URL,
        headers={"Authorization": f"Client-ID {imgur_client_id}"},
        data={"image": encoded, "type": "base64"}
    )
    res.raise_for_status()
    imgur_data = res.json()["data"]
    print(f"✅ Image uploaded to Imgur: {imgur_data['link']}")
    return imgur_data


def delete_from_imgur(deletehash, imgur_client_id):
    print(f"🧹 Deleting image from Imgur using deletehash: {deletehash}")
    res = requests.delete(
        IMGUR_DELETE_URL.format(deletehash=deletehash),
        headers={"Authorization": f"Client-ID {imgur_client_id}"}
    )
    res.raise_for_status()
    print("✅ Image deleted from Imgur.")
