# -*- coding:UTF-8 -*-
from django import template
from bellawiki import lunar
register = template.Library()

@register.filter(name='lunartag')
def lunartag(field):
	ld = lunar.get_lunar_date(field.year, field.month, field.day)
	return str(ld[1]) + "月" + str(ld[2]) + "日"
