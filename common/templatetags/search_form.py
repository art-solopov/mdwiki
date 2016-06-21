from django import template

register = template.Library()

@register.inclusion_tag('common/search_form.html')
def search_form():
    return {}
