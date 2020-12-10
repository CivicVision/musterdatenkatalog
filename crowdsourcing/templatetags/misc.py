from django import template

register = template.Library()

@register.filter
def join_by_attr(the_list, attr_name, separator=', '):
    return separator.join(getattr(i, attr_name) for i in the_list)

@register.simple_tag
def setvar(val=None):
    return val
