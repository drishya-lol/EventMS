from django import template

register = template.Library()

@register.filter(name='is_EventPlanner')
def is_EventPlanner(user):
    return user.groups.filter(name='EventPlanner').exists()

@register.filter(name='is_Admin')
def is_Admin(user):
    return user.groups.filter(name='Admin').exists()

@register.filter(name='is_Vendor')
def is_Vendor(user):
    return user.groups.filter(name='Vendor').exists()
