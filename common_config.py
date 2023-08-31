import os
from dotenv import load_dotenv

load_dotenv()

"""Temporary config credentials for testing purposes"""
SENDINBLUE_API_KEY = os.environ.get("SENDINBLUE_API_KEY")
SENDINBLUE_API_URL = os.environ.get("SENDINBLUE_API_URL")

"""Email config"""
SENDGRID_API_KEY = os.environ.get("SENDGRID_KEY")
SENDGRID_API_URL = os.environ.get("SENDGRID_API_URL")
