from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=True)
def nav_link(context, url_name):
    request = context.get('request')
    url = reverse(url_name)
    if request and request.resolver_match and request.resolver_match.url_name == url_name:
        return mark_safe('class="active"')
    return mark_safe(f'href="{url}"')