import re
from django import template

register = template.Library()

PASSWORD_SET_REGEX = "Password is not set for"

@register.filter
def username_from_email(email):
    return email.split('@')[0]

@register.filter
def is_password_set_message(message):
    if re.search(PASSWORD_SET_REGEX, str(message)):
        return True
    return False

@register.filter
def customise_url(image_url, size):
    google_drive_domain = 'drive.google.com'
    google_user_content = "lh3.googleusercontent.com"
    if google_drive_domain in image_url:
        image_url = image_url.replace('file/d/', 'thumbnail?id=')
        image_url = image_url.replace('/view', f'&sz=s{size}')
    elif google_user_content:
        pattern = r'(?<=s)\d+(?=-c)'
        image_url = re.sub(pattern, str(size), image_url)

    return image_url