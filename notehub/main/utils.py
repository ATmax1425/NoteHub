import os
import json
import random
import string
import base64
import secrets
from os.path import join

from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

EMAIL_CONFIG_FILE = 'email_config.json'

with open(join(settings.BASE_DIR, EMAIL_CONFIG_FILE)) as file:
    EMAIL_CONFIG = json.load(file)
    SENDER = EMAIL_CONFIG['EMAIL_HOST_USER']

SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR, 'google-drive-api-key.json')
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def generate_verification_code():
    # Define the character sets
    special_characters = "!@#$%^&*()-_=+"
    uppercase_characters = string.ascii_uppercase
    lowercase_characters = string.ascii_lowercase
    digits = string.digits

    # Ensure at least one character from each set is included
    code = [
        random.choice(special_characters),
        random.choice(uppercase_characters),
        random.choice(lowercase_characters),
        random.choice(digits)
    ]

    # Fill the rest of the code with random characters from all sets
    all_characters = special_characters + uppercase_characters + lowercase_characters + digits
    while len(code) < 6:
        code.append(random.choice(all_characters))

    # Shuffle the list to ensure randomness
    random.shuffle(code)

    # Convert list to string and return
    return ''.join(code)

def upload_to_drive(file_path, file_name):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, mimetype='image/jpeg')

    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    service.permissions().create(fileId=file.get('id'), body=permission).execute()
    url = f"https://drive.google.com/file/d/{file.get('id')}/view"

    return url

def send_email(recipients, subject, template, metadata):
    try:
        html_content = render_to_string(f"email/{template}", metadata)
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(subject, text_content, SENDER, recipients)
        email.content_subtype = 'html'  # Main content is now text/html
        email.attach_alternative(html_content, "text/html")
        email.send()
        return True
    except Exception as exc:
        print('Error while sending the email', exc)
    return False

def encode_with_random_salt(original_string):
    encoded_bytes = base64.urlsafe_b64encode(original_string.encode())
    encoded_string = encoded_bytes.decode()
    salt = secrets.token_urlsafe(8)
    random_encoded_string = f"{salt}{encoded_string}"
    return random_encoded_string

def decode_with_random_salt(encoded_string):
    actual_encoded_string = encoded_string[11:]
    decoded_bytes = base64.urlsafe_b64decode(actual_encoded_string.encode())
    decoded_string = decoded_bytes.decode()
    return decoded_string

def send_verification_email(user, ):
    cache.set(f"verification_status:{user.email}", 'pending')
    recipient = [user.email]
    subject = 'Welcome Onboard!'
    template = 'welcome_user.html'
    metadata = {'user': user, 'url': f'{settings.PROJECT_URL}/{encode_with_random_salt(user.email)}/verify'}
    send_email(recipient, subject, template, metadata)
