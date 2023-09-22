from django import template

register = template.Library()

@register.simple_tag
def get_username(request):
    return request.session.get('username', '')