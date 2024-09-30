from django import template

register = template.Library()

@register.filter
def star_ratings(value):
    return "⭐️" * value