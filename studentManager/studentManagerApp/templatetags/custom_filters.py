from django import template
register=template.Library()
@register.filter(name='get_index')
def get_index(sequence, index):
    try:
        return sequence[index]
    except (IndexError, TypeError ):
        return None