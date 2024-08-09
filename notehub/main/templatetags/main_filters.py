import re
import math
from django import template
from datetime import datetime

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
        image_url = re.sub(r'file/d/', 'thumbnail?id=', image_url)
        image_url = re.sub(r'/view', f'&sz=s{size}', image_url)
    elif google_user_content:
        pattern = r'(?<=s)\d+(?=-c)'
        image_url = re.sub(pattern, str(size), image_url)

    return image_url

@register.filter
def time_ago(timestamp):
    now = datetime.now()
    post_date = datetime.fromtimestamp(timestamp)
    diff_in_seconds = int((now - post_date).total_seconds())

    seconds = diff_in_seconds
    minutes = diff_in_seconds // 60
    hours = diff_in_seconds // 3600
    days = diff_in_seconds // 86400
    months = diff_in_seconds // (86400 * 30.44)
    years = diff_in_seconds // (86400 * 365.25)

    if years > 0:
        return "1 year ago" if years == 1 else f"{years} years ago"
    elif months > 0:
        return "1 month ago" if months == 1 else f"{months} months ago"
    elif days > 0:
        return "1 day ago" if days == 1 else f"{days} days ago"
    elif hours > 0:
        return "1 hour ago" if hours == 1 else f"{hours} hours ago"
    elif minutes > 0:
        return "1 minute ago" if minutes == 1 else f"{minutes} minutes ago"
    else:
        return "1 second ago" if seconds == 1 else f"{seconds} seconds ago"

@register.filter
def convert_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    size = round(size_bytes / math.pow(1024, i), 2)
    
    return f"{size} {size_names[i]}"

@register.filter
def convert_drive_file_url(source_url):
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', source_url)
    if match:
        file_id = match.group(1)
        target_url = f"https://drive.usercontent.google.com/u/0/uc?id={file_id}&export=download"
        return target_url
    return None