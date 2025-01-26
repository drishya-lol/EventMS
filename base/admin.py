from django.contrib import admin
from .models import Event, EventCategory, VendorCategory, Vendor, TicketType, EventRegistration
# Register your models here.
admin.site.register(Event)
admin.site.register(EventCategory)
admin.site.register(VendorCategory)
admin.site.register(Vendor)
admin.site.register(TicketType)
admin.site.register(EventRegistration)