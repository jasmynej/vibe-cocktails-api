import boto3
from core.config import settings


s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)

def upload_image_to_s3(
        file_bytes: bytes,
        content_type: str,
        folder: str = "cocktails",
        name: str = 'image'
    ) -> str:
    file_name = f"{folder}/{name}"

    s3_client.put_object(
        Bucket=settings.AWS_S3_BUCKET,
        Key=file_name,
        Body=file_bytes,
        ContentType=content_type,
    )

    return f"https://{settings.AWS_S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{file_name}"