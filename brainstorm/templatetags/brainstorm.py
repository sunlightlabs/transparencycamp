from django import template

register = template.Library()


@register.filter
def can_post_in(user, subsite):
    return subsite.user_can_post(user)


@register.filter
def simpleformat(str, val):
    try:
        return str.format(val)
    except:
        return ""
