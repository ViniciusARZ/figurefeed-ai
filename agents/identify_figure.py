import json
import litellm
import base64

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def identify_figure(image_b64: str, api_key: str, identifier_model: str) -> str:
    litellm.api_key = api_key

    messages = [
        {
            "role": "system",
            "content": (
                "You are an anime figure identifier. "
                "Given a figure photo, return metadata in this exact format:\n"
                "`Characters; Name of the Figure; Manufacturer`"
            )
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_b64}"
                    }
                },
                {
                    "type": "text",
                    "text": "Please return only the required format, no extra text."
                }
            ]
        }
    ]

    response = litellm.completion(
        model=identifier_model,
        messages=messages
    )

    return response["choices"][0]["message"]["content"].strip()
