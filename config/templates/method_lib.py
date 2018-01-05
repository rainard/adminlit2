#!coding=utf-8
from django import template
register = template.Library()


@register.simple_tag
def get_fileds_value(field,key):
    return field.__dict__[key]