from django import template
register=template.Library()
@register.filter(name="get_reply")
def get_reply(dict, key):
    return dict.get(key)