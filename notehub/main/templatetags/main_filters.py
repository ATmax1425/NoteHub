from django import template

register = template.Library()

@register.filter
def username_from_email(email):
    return email.split('@')[0]
