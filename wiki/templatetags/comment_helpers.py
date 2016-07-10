from django import template

register = template.Library()

@register.simple_tag
def comment_style(comment):
    styles = {
        'margin-left': _px((comment.depth - 1) * 30),
    }
    return ';'.join("{0}: {1}".format(k, v) for k, v in styles.items())

def _px(value):
    return "{0}px".format(value)
