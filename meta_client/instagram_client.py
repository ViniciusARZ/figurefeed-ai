import requests
import json

def post_image_to_instagram(image_url: str, caption: str, access_token: str, ig_user_id: str):
    print("📦 Creating Instagram media container...")
    create_url = f'https://graph.facebook.com/v19.0/{ig_user_id}/media'
    create_params = {
        'image_url': image_url,
        'caption': caption,
        'access_token': access_token
    }
    create_res = requests.post(create_url, data=create_params)
    create_data = create_res.json()

    if 'id' not in create_data:
        raise Exception(f"Failed to create media: {create_data}")

    media_id = create_data['id']
    print(f"✅ Media container created: {media_id}")

    print("📤 Publishing to Instagram...")
    publish_url = f'https://graph.facebook.com/v19.0/{ig_user_id}/media_publish'
    publish_res = requests.post(publish_url, data={
        'creation_id': media_id,
        'access_token': access_token
    })
    publish_data = publish_res.json()

    if 'id' in publish_data:
        return publish_data['id']
    else:
        raise Exception(f"Failed to publish: {publish_data}")
