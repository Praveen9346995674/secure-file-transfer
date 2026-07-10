import os
import boto3
from cryptography.fernet import Fernet
import config

KEY_FILE = "secret.key"

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key

key = load_key()
cipher = Fernet(key)

# AWS S3 Client
s3 = boto3.client(
    "s3",
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    region_name=config.AWS_REGION
)

def encrypt_file(data):
    return cipher.encrypt(data)

def decrypt_file(data):
    return cipher.decrypt(data)

# Upload encrypted file to AWS S3
def upload_to_s3(data, filename):
    s3.put_object(
        Bucket=config.AWS_BUCKET_NAME,
        Key=filename,
        Body=data
    )

# Download encrypted file from AWS S3
def download_from_s3(filename):
    response = s3.get_object(
        Bucket=config.AWS_BUCKET_NAME,
        Key=filename
    )
    return response["Body"].read()