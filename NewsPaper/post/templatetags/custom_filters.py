from django import template
from post.censor.check_text import return_clear_text

register = template.Library()


@register.filter(name='censor')
def censor(value):
    return return_clear_text(str(value))
    