from django import template
from num2words import num2words
register = template.Library()

@register.simple_tag
def get_numeric_word(number):
    return num2words(number)

@register.simple_tag
def get_numeric_word_label(number):
    return str(num2words(number)).title().replace('-', ' ')    
@register.filter(name='times') 
def times(number):
    return range(1, number+1)
    
    
@register.simple_tag(name='multiply')
def multiply(table_num, unit, *args, **kwargs):
    # you would need to do any localization of the result here
    return table_num * unit