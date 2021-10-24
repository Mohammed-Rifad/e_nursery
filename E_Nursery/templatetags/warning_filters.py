from django import template
from django.template.defaultfilters import stringfilter
register=template.Library()


@stringfilter
def get_msg(qty,stock):
    
    if stock == 0:
        return "Temporarily Not Available"
    elif int(qty)>int(stock):
        return "Only "+str(stock)+" Items Left"
    
register.filter(get_msg)