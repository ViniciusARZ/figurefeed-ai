from google_photos_client.google_photos_client import GooglePhotosClient

client = GooglePhotosClient(
    credentials_path='google_credentials.json',
    token_path='token.json'
)

print("📂 Fetching albums...")
albums = client.list_albums()

for album in albums:
    print(f"- {album['title']} (ID: {album['id']})")
