from django import template

register = template.Library()

from hoarder.backends import get_backends
from hoarder import _get_visitor_id

@register.simple_tag(takes_context=True)
def tracking_code(context):
    context.push()
    context['visitor_id'] = _get_visitor_id(context['request'])
    try:
        return ''.join([b.get_tracking_code(context) for b in get_backends()])
    finally:
        context.pop()

