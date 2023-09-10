from common_config import (
    SENDINBLUE_API_KEY,
    SENDINBLUE_API_URL,
    SENDGRID_API_KEY,
    SENDGRID_API_URL,
)
import requests
from rest_framework_simplejwt.tokens import RefreshToken
import random
import string
import boto3
from botocore.exceptions import ClientError


# Password check function for users
def password_check(password):
    if len(password) < 8:
        return False
    has_uppercase = False
    for char in password:
        if char.isupper():
            has_uppercase = True
            break
    if not has_uppercase:
        return False
    has_lowercase = False
    for char in password:
        if char.islower():
            has_lowercase = True
            break
    if not has_lowercase:
        return False
    has_digit = False
    for char in password:
        if char.isdigit():
            has_digit = True
            break
    if not has_digit:
        return False
    special_chars = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
    has_special = False
    for char in password:
        if char in special_chars:
            has_special = True
            break
    if not has_special:
        return False
    return True


# JWT token generator function
def get_tokens_for_user(user):
    """This function generates JWT tokens for a user"""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def send_email_with_sendgrid(to_email, content):
    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "personalizations": [
            {"to": [{"email": to_email}], "subject": "Test Email from EVENTS.az"}
        ],
        "from": {"email": "krnraj002@gmail.com"},
        "content": [{"type": "text/plain", "value": content}],
    }

    try:
        response = requests.post(SENDGRID_API_URL, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP errors
        print("Email sent successfully.")  # Print statement added here
        return True  # Email sent successfully
    except requests.exceptions.RequestException as e:
        print("Error sending email:", e)
        return False


def generate_random_password(length=10):
    if length < 4:
        raise ValueError("Password length must be at least 4 characters")

    lowercase_letters = string.ascii_lowercase
    uppercase_letter = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    symbol = random.choice(string.punctuation)

    # Ensure that the remaining characters in the password are lowercase letters
    remaining_length = length - 4
    password = [random.choice(lowercase_letters) for _ in range(remaining_length)]

    # Shuffle the password characters to make it random
    random.shuffle(password)

    # Insert the uppercase letter, digit, and symbol at random positions
    password.insert(random.randint(0, remaining_length), uppercase_letter)
    password.insert(random.randint(0, remaining_length), digit)
    password.insert(random.randint(0, remaining_length), symbol)

    # Convert the password list to a string
    password = "".join(password)

    return password


def upload_S3_image(folder_name, request, image_name):
    Access_key = "AKIASNPAKV5UAXCNWAG4"
    Secret_key = "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"

    try:
        s3_session = boto3.Session(
            aws_access_key_id=Access_key,
            aws_secret_access_key=Secret_key,
            region_name="us-east-1",
        )
        s3_client = s3_session.client("s3")
        bucket_name = "events-bucket-az"  # Just the bucket name without any folder path

        # Get the uploaded file from the request
        uploaded_file = request.FILES["image"]
        # Specify the S3 key with the folder path and image name
        s3_key = folder_name + image_name

        # Upload the file object to S3
        s3_client.upload_fileobj(uploaded_file, bucket_name, s3_key)

        # Generate the S3 URL
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"

        return True, s3_url
    except Exception as e:
        return {"message": str(e)}


# def create_order(amount):
#     PAYRIFF_API_KEY = "982A46D2D237430493F4E603D2C588CE"
#     PAYRIFF_URL = "https://api.payriff.com/api/v2/createOrder"

#     headers = {
#         "Authorization": f"{PAYRIFF_API_KEY}",
#         "Content-Type": "application/json",
#     }
#     data = {
#         "body": {
#             "amount": amount,
#             "approveURL": "https://16a5-5-134-55-140.ngrok-free.app/approveURL/",
#             "cancelURL": "string",
#             "cardUuid": "string",
#             "currencyType": "AZN",
#             "declineURL": "string",
#             "description": "string",
#             "directPay": True,
#             "installmentPeriod": 0,
#             "installmentProductType": "BIRKART",
#             "language": "AZ",
#             "senderCardUID": "string",
#         },
#         "merchant": "ES1092133",
#     }
#     try:
#         response = requests.post(PAYRIFF_URL, headers=headers, data=json.dumps(data))
#         response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
#         response_data = response.json()
#         return response_data
#     except requests.exceptions.RequestException as e:
#         print("Request failed:", e)
#         return None


# def upload_S3_image(folder_name, image_path, image_name):
#     Access_key = "AKIASNPAKV5UAXCNWAG4"
#     Secret_key = "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"
#     try:
#         s3_session = boto3.Session(
#             aws_access_key_id=Access_key,
#             aws_secret_access_key=Secret_key,
#             region_name="us-east-1",
#         )
#         s3_client = s3_session.client("s3")
#         bucket_name = "events-bucket-az"  # Just the bucket name without any folder path
#         file_name = (
#             image_path  # Replace with the actual file path on your local machine
#         )
#         s3_key = folder_name + image_name  # Include the folder path in the S3 key
#         response = s3_client.upload_fileobj(file_name, bucket_name, s3_key)
#         s3_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
#         print(s3_url)
#         return True
#     except Exception as e:
#         return {"message": "No data found"}
