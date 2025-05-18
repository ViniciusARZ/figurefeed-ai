from agents.identify_figure import encode_image, identify_figure
from agents.crew import FigureCaptionCrew
import json
import base64

def crew_get_caption(
    image_bytes: bytes,
    identifier_model: str = "gpt-4-turbo",
    caption_model: str = "gpt-3.5-turbo",
    config_path: str = "config.json",
    api_key: str = "",
    verbose: bool = True
):
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    figure_metadata = identify_figure(image_b64, identifier_model=identifier_model, api_key=api_key)

    with open(config_path) as f:
        cfg = json.load(f)

    crew_runner = FigureCaptionCrew(
        caption_model=caption_model,
        api_key=cfg["openai_api_key"],
        verbose=verbose
    )

    crew_instance = crew_runner.crew()
    result = crew_instance.kickoff({
        "figure_metadata": figure_metadata
    })

    return result

if __name__ == "__main__":
    caption = crew_get_caption("test_image.jpg")
    print("\n📸 Final Caption:\n", caption)
