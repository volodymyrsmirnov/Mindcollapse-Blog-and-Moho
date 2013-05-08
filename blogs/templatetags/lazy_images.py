import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@stringfilter
def lazy_images(value):
    for match in re.finditer('<img.*?class="lazy".*?>', value):
        replace_from = match.group(0)
        replace_to = match.group(0).replace('src=', 'src="/static/blog/grey.gif" data-original=')
        value = value.replace(replace_from, replace_to)

    return value

lazy_images.is_safe = True

register.filter('lazy_images', lazy_images)
