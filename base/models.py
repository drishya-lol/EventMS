from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    max_attendees = models.IntegerField()
    registrations = models.IntegerField(default=0)
    categories = models.ManyToManyField('EventCategory')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    vip_cost = models.IntegerField(default=2000, null=True)
    standard_cost = models.IntegerField(default=500, null=True)
    
    def __str__(self):
        return self.name
    
class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    attendee_name = models.CharField(max_length=100)
    attendee_email = models.EmailField()
    ticket_type = models.ForeignKey('TicketType', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.attendee_name} - {self.event.name}"
    
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    services_offered = models.TextField()
    pricing = models.DecimalField(max_digits=10, decimal_places=2)
    contact_info = models.CharField(max_length=100)
    website = models.URLField(null=True)
    categories = models.ManyToManyField('VendorCategory')
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
class VendorCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class VendorAssignment(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='assignments')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    
class VendorPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    punctuality = models.IntegerField()
    sercive_quality = models.IntegerField()
    feedback = models.TextField()
    
class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)
    ticket_type = models.ForeignKey('TicketType', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1000, null=True)
    unique_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.ticket_type.name} - {self.event.name}"
    
class TicketType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=100, choices=[
        ('Pending', 'Pending'), ('Paid', 'Paid'), ('Cancelled', 'Cancelled')
        ], default='Pending')
    
    def __str__(self):
        return f"Invoice {self.id} for {self.client.username}"
    
class Logistics(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    vendor =  models.ForeignKey(Vendor, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    
class Inventory(models.Model):
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    
class EventReview(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comments = models.TextField()
    is_approved = models.BooleanField(default=False)
    
class VendorFeedback(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comments = models.TextField()
    
class Report(models.Model):
    type = models.CharField(max_length=100)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)