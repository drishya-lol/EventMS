from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    max_attendees = models.IntegerField()
    categories = models.ManyToManyField('EventCategory')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    
    def __str__(self):
        return self.name
    
class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    attendee_name = models.CharField(max_length=100)
    attendee_email = models.EmailField()
    ticket_type = models.CharField(max_length=100)
    
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
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unique_code = models.CharField(max_length=100)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

class Invoice(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=100)
    
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