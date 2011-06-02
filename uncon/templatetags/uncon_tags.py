from django import template
from transparencycamp.uncon.models import Tweet
import re

register = template.Library()

class UpdatesNode(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name
    def render(self, context):
        context[self.var_name] = Tweet.objects.filter(user__screen_name='TCampDC')
        return ''

@register.tag(name="updates")
def do_updates(parse, token):
    parts = token.contents.split()
    return UpdatesNode(parts[-1])