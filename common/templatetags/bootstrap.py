from django import template

register = template.Library()

WIDGET_ATTRIBUTES = {'class': 'form-control'}

@register.inclusion_tag('common/bootstrap/form.html')
def bootstrap_form(form, **kwargs):
    action = kwargs.get('action', '')
    method = kwargs.get('method', 'POST')
    submit = kwargs.get('submit', 'Submit')
    return {
        'form': form,
        'action': action,
        'method': method,
        'submit': 'submit'
    }

@register.simple_tag
def bootstrap_widget(field):
    return field.label_tag() + field.as_widget(attrs=WIDGET_ATTRIBUTES)
