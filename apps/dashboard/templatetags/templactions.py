import re
from django.template.library import Library

register = Library()


@register.simple_tag(takes_context=True)
def activeclass(context, slug):
    request = context['request']
    if re.match(r'^.*'+slug, request.META['PATH_INFO'].strip(' /')):
        return ' class=active'
    else:
        return ''
