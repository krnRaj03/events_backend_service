from common_config import SENDINBLUE_API_KEY, SENDINBLUE_API_URL
import requests
from rest_framework_simplejwt.tokens import RefreshToken


# Password check function
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
