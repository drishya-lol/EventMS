from django import template
from ..models import EventRegistration
register = template.Library()

@register.filter(name='is_EventPlanner')
def is_EventPlanner(user):
    return user.groups.filter(name='Event Planner').exists()

@register.filter(name='is_Admin')
def is_Admin(user):
    return user.groups.filter(name='Admin').exists()

@register.filter(name='is_Vendor')
def is_Vendor(user):
    return user.groups.filter(name='Vendor').exists()

@register.filter(name='is_Client')
def is_Client(user):
    return user.groups.filter(name='Client').exists()

@register.filter(name='is_approved')
def is_approved(review):
    return review.is_approved