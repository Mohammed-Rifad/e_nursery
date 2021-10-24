from django import template

register=template.Library()


@register.simple_tag
def get_msg(array,index):
    return array[index]
    
register.filter(get_msg)