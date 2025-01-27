from django import forms
from .models import Event, EventCategory, EventRegistration, Vendor, VendorCategory, VendorPerformance, Ticket, VendorAssignment, TicketType, Logistics, Inventory, EventReview, VendorFeedback
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import RadioSelect

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
        fields = ['vendor']
        widgets = {
            'vendor': forms.Select(attrs={'class': 'form-control'})
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

class EventReviewForm(forms.ModelForm):
    class Meta:
        model = EventReview
        fields = ['rating', 'comments']
        widgets = {
            'rating': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 1,
                    'max': 5,
                    'placeholder': 'Rate between 1 and 5',
                }
            ),
            'comments': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Share your thoughts about the event...',
                    'rows': 4,
                }
            ),
        }

class VendorFeedbackForm(forms.ModelForm):
    class Meta:
        model = VendorFeedback
        fields = ['rating', 'comments']
        widgets = {
            'rating': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 1,
                    'max': 5,
                    'placeholder': 'Rate between 1 and 5',
                }
            ),
            'comments': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Share your thoughts about the vendor...',
                    'rows': 4,
                }
            ),
        }
        
class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your current password'
        })
    )
    
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        })
    )
    
    confirm_password = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError({
                    'confirm_password': 'The new passwords do not match.'
                })
            
            # Check if new password is different from current password
            if 'password' in cleaned_data and new_password == cleaned_data['password']:
                raise forms.ValidationError({
                    'new_password': 'New password must be different from current password.'
                })

        return cleaned_data