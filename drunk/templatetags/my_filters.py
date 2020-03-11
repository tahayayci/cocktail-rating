from django import template

register = template.Library()

@register.filter(name='times') 
def times(number):
    if number == None:
        return range(0)
    return range(int(number))

@register.filter(name='fivemtimes')
def five_minus_times(number):
    if number == None:
        return range(0)
    return range(int(5 - number))