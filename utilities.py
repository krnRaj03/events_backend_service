from common_config import (
    SENDGRID_API_KEY,
    SENDGRID_API_URL,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
)
import requests
from rest_framework_simplejwt.tokens import RefreshToken
import random, json, string
import boto3
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from PIL import Image, ImageDraw, ImageFont
import qrcode
import requests
from io import BytesIO


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


def send_email_sendgrid(to_email, content):
    # Replace with your SendGrid API key
    api_key = SENDGRID_API_KEY

    # Create the email message
    message = Mail(
        from_email="mhertz.az@gmail.com",  # Replace with your sender email
        to_emails=to_email,
        subject="Test Email from EVENTS.az",
        html_content=content,
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print("Email sent successfully!")
        print("Status Code:", response.status_code)

    except Exception as e:
        print("Error:", str(e))


def generate_random_password(length=10):
    if length < 4:
        raise ValueError("Password length must be at least 4 characters")

    lowercase_letters = string.ascii_lowercase
    uppercase_letter = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)

    # Define a custom string of symbols without double quotes
    symbols = "".join(char for char in string.punctuation if char != '"')
    symbol = random.choice(symbols)

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
    # Access_key = AWS_ACCESS_KEY_ID
    # Secret_key = AWS_SECRET_ACCESS_KEY

    # try:
    s3_session = boto3.Session(
        aws_access_key_id="AKIASNPAKV5UAXCNWAG4",
        aws_secret_access_key="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",
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
    # except Exception as e:
    #     return False, str(e)


def create_order(amount):
    PAYRIFF_API_KEY = "982A46D2D237430493F4E603D2C588CE"
    PAYRIFF_URL = "https://api.payriff.com/api/v2/createOrder"

    headers = {
        "Authorization": f"{PAYRIFF_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "body": {
            "amount": amount,
            "approveURL": "https://16a5-5-134-55-140.ngrok-free.app/approveURL/",
            "cancelURL": "string",
            "cardUuid": "string",
            "currencyType": "AZN",
            "declineURL": "string",
            "description": "string",
            "directPay": True,
            "installmentPeriod": 0,
            "installmentProductType": "BIRKART",
            "language": "AZ",
            "senderCardUID": "string",
        },
        "merchant": "ES1092133",
    }
    try:
        response = requests.post(PAYRIFF_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        response_data = response.json()
        return response_data
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None


def generate_ticket_with_qr(ticket_url, data):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=2,
    )

    # Add the data to the QR code
    qr.add_data(data)

    # Compile the QR code
    qr.make(fit=True)

    # Create a PIL image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Download the background image from the URL
    response = requests.get(ticket_url)
    if response.status_code == 200:
        # Open the image from the downloaded content
        background = Image.open(BytesIO(response.content))

        # Calculate the position to place the QR code in the bottom right corner
        x = background.width - img.width - 880  # Adjust the horizontal position
        y = background.height - img.height - 300  # Adjust the vertical position

        # Paste the QR code onto the background image
        background.paste(img, (x, y))

        # Create ImageDraw instance
        draw = ImageDraw.Draw(background)

        # Specify font-size and color
        font_size = 80
        font_color = "rgb(255,255,255)"  # black color

        # Specify font (make sure the .ttf font file is in your directory)
        font = ImageFont.truetype("arial.ttf", font_size)

        # Position of the text
        text_position = (300, 250)  # (x, y)

        # Add dynamic text to image
        draw.text(text_position, data, fill=font_color, font=font)

        # Save the image to a file (optional)
        background.save("newQr.png")

        # Display the image using Pillow
        background.show()
    else:
        print("Failed to download the background image.")
