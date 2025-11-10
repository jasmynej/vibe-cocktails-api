import base64
import core.config as config
from openai import OpenAI, AsyncOpenAI

settings = config.settings

def gen_cocktail_image(prompt: str):
    client = OpenAI(api_key=settings.OPEN_AI_KEY)
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
    )
    if not response.data or not response.data[0].b64_json:
        raise ValueError(f"No base64 image data returned for prompt: {prompt}")

    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    return image_bytes
