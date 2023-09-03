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


# Send email using SendinBlue API
def send_email_via_sendinblue(to, body):
    headers = {"Content-Type": "application/json", "api-key": SENDINBLUE_API_KEY}
    data = {
        "to": [{"email": to}],
        "subject": "Welcome to Events Az!",
        "htmlContent": body,
        "sender": {"name": "Your Name", "email": "krnraj002@gmail.com"},
    }
    response = requests.post(SENDINBLUE_API_URL, headers=headers, json=data)
    if response.status_code == 201:
        print("Email sent successfully!")
    else:
        print("Failed to send email. Status Code: {}".format(response.status_code))


# Send email (Forgot Password) using SendinBlue API
def send_forget_password_email(to, body):
    headers = {"Content-Type": "application/json", "api-key": SENDINBLUE_API_KEY}
    data = {
        "to": [{"email": to}],
        "subject": "Forget Password Mail.",
        "htmlContent": body,
        "sender": {"name": "Your Name", "email": "krnraj002@gmail.com"},
    }
    response = requests.post(SENDINBLUE_API_URL, headers=headers, json=data)
    if response.status_code == 201:
        print("Email sent successfully!")
    else:
        print("Failed to send email. Status Code: {}".format(response.status_code))


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


# # Example usage:
# password = generate_random_password()
# print(password)
