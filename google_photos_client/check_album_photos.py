import json
from google_photos_client.google_photos_client import GooglePhotosClient

client = GooglePhotosClient(
    credentials_path='google_credentials.json',
    token_path='token.json'
)

with open('config.json') as f:
    config = json.load(f)

album_id = config['google_photos_album_id']

print(f"📸 Fetching media from album: {album_id}")
items = client.get_photos_from_album(album_id, page_size=5)

for item in items:
    print(f"- {item['filename']}")
    print(f"  URL: {item['baseUrl']}=w1080")
