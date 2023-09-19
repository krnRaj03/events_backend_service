import os
from dotenv import load_dotenv

load_dotenv()

"""Email config"""
SENDGRID_API_KEY = os.environ.get("SENDGRID_KEY")
SENDGRID_API_URL = os.environ.get("SENDGRID_API_URL")

"""AWS config"""
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
