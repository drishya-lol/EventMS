from django import forms
from .models import Event, EventCategory, EventRegistration, Vendor, VendorCategory, VendorPerformance, Ticket, VendorAssignment, TicketType, Logistics, Inventory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first-name': forms.TextInput(attrs={'class': 'form-control'}),
            'last-name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(),
        }
        
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        
class EventCreationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'max_attendees', 'categories', 'vip_cost', 'standard_cost']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type':'time', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'max_attendees': forms.NumberInput(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'vip_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'standard_cost': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'services_offered', 'pricing', 'contact_info', 'website', 'categories']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'services_offered': forms.Textarea(attrs={'class': 'form-control'}),
            'pricing': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        
class VendorAssignmentForm(forms.ModelForm):
    class Meta:
        model = VendorAssignment
        fields = ['vendor', 'is_available']
        widgets = {
            'vendor': forms.Select(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        
class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['ticket_type']
        widgets = {
            # 'event': forms.Select(attrs={'class': 'form-control'}),
            'ticket_type': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EventRegistrationForm, self).__init__(*args, **kwargs)
        if user:
            self.instance.event = Event.objects.get(pk=self.initial['event'])
            self.instance.attendee_name = f"{user.first_name} {user.last_name}"
            self.instance.attendee_email = user.email
            
        ticket_types = TicketType.objects.all()
        self.fields['ticket_type'].queryset = ticket_types

class LogisticsForm(forms.ModelForm):
    class Meta:
        model = Logistics
        fields = ['category']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['item_name', 'quantity']
        widgets = {
            'item_name': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }