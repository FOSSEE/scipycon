from django import template

register = template.Library()

def choice(choices, value):
    return choices[value]

register.filter('choice', choice)
