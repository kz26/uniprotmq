from django import template
from django.core.urlresolvers import *
import re
register = template.Library()

class ActiveNavNode(template.Node):
    def __init__(self, urls):
        self.urls = urls
    def render(self, context):
        request = context['request']
        for u in self.urls:
            req = resolve(request.path)
            if u == req.url_name:
                return 'active'
        return ""
             

@register.tag
def active_nav(parse, token):
    args = token.split_contents()
    template_tag = args[0]
    if len(args) < 2:
        raise template.TemplateSyntaxError("%r tag requires at least one argument" % (token.contents.split()[0]))
    return ActiveNavNode(args[1:])
