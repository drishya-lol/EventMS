from django.contrib import admin
from .models import Event, EventCategory, VendorCategory, Vendor, TicketType, EventRegistration, Inventory, Logistics, InventoryCategory
# Register your models here.
admin.site.register(Event)
admin.site.register(EventCategory)
admin.site.register(VendorCategory)
admin.site.register(Vendor)
admin.site.register(TicketType)
admin.site.register(EventRegistration)
admin.site.register(Logistics)
admin.site.register(InventoryCategory)