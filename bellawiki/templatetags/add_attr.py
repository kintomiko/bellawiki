from django import template
register = template.Library()

@register.filter(name='add_attr')
def add_attr(field, attr):
	key=attr.split(':')[0]
	value=attr.split(':')[1]
	return field.as_widget(attrs={key:value})