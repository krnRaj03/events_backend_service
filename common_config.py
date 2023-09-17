import os
from dotenv import load_dotenv

load_dotenv()

"""Email config"""
SENDGRID_API_KEY = os.environ.get("SENDGRID_KEY")
SENDGRID_API_URL = os.environ.get("SENDGRID_API_URL")
