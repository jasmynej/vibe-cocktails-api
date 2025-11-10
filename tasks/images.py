from core.s3 import upload_image_to_s3
from lib.images import gen_cocktail_image
from sqlmodel import Session, select
from core.db import engine
from models.cocktail import Cocktail
import uuid


def generate_cocktail_image(cocktail_id: int):
    with Session(engine) as session:
        cocktail = session.exec(select(Cocktail).where(Cocktail.id == cocktail_id)).first()
        if not cocktail:
            return {"error": f"Cocktail {cocktail_id} not found"}

        prompt = (
            f"A flat drawing of the cocktail '{cocktail.name}', "
            f"visually inspired by: {cocktail.description}. "
            "No text or cluttered background."
        )

        image_bytes = gen_cocktail_image(prompt)
        image_name = f"{uuid.uuid4()}-{cocktail.name.replace(' ', '_')}.png"
        url = upload_image_to_s3(image_bytes, "image/png", name=image_name, folder="cocktail-images")

        cocktail.image = url
        session.add(cocktail)
        session.commit()

        print({"status": "success", "cocktail_id": cocktail_id, "image_url": url})
        return True