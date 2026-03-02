from django import template

register = template.Library()

@register.filter(name='split')
def split(value, separator=','):
    """
    Matnni ajratish
    """
    if value:
        return value.split(separator)
    return []

@register.filter(name='trim')
def trim(value):
    """
    Bo'sh joylarni olib tashlash
    """
    if value:
        return value.strip()
    return value

@register.filter(name='intcomma')
def intcomma(value):
    """
    Raqamlarni formatlash (1000 -> 1,000)
    """
    try:
        value = int(value)
        return "{:,}".format(value)
    except (ValueError, TypeError):
        return value

@register.filter(name='shorten_number')
def shorten_number(value):
    """
    Katta raqamlarni qisqartirish
    1000 -> 1K
    1000000 -> 1M
    1000000000 -> 1B
    """
    try:
        value = int(value)
        if value >= 1000000000:
            return f"{value/1000000000:.1f}B"
        elif value >= 1000000:
            return f"{value/1000000:.1f}M"
        elif value >= 1000:
            return f"{value/1000:.1f}K"
        else:
            return str(value)
    except (ValueError, TypeError):
        return value
