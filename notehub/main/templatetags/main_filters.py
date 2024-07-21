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
