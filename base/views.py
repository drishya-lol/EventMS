from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import UserRegistrationForm, LoginForm, EventCreationForm, VendorForm, VendorAssignmentForm, UserForm, EventRegistrationForm, LogisticsForm, InventoryForm, EventReviewForm, VendorFeedbackForm, ChangePasswordForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import Event, EventCategory, EventRegistration, Vendor, VendorPerformance, Ticket, VendorAssignment, Invoice, Logistics, Inventory, EventReview, VendorFeedback
from django.views.generic import DetailView, ListView
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.core.mail import send_mail
from reportlab.pdfgen import canvas
from django.conf import settings
from django.utils.crypto import get_random_string
from django_filters.views import FilterView
import django_filters
from django.db.models import Q, Sum, Count
import datetime

# Create your views here.

# def home(request):
#     return render(request, 'home.html')

def userRegistration(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        clientGroup = Group.objects.get(name='Client')
        password = request.POST.get('password')
        newpassword = make_password(password)
        data = request.POST.copy()
        data['password'] = newpassword
        form = UserRegistrationForm(data)
        if form.is_valid():
            user = form.save()
            user.groups.add(clientGroup)
            user.save()
            return redirect('login')
        else:
            return render(request, 'register.html', context = {'form': form})
    data = {'form': form}
    return render(request, 'register.html', context = data)

@login_required
@user_passes_test(lambda u: u.is_staff)
def register_eventPlanner(request):
    if request.user.groups.filter(name='Admin').exists():
        form = UserRegistrationForm()
        if request.method == 'POST':
            eventManagerGroup = Group.objects.get(name='Event Planner')
            password = request.POST.get('password')
            newpassword = make_password(password)
            data = request.POST.copy()
            data['password'] = newpassword
            form = UserRegistrationForm(data)
            if form.is_valid():
                user = form.save()
                user.groups.add(eventManagerGroup)
                user.save()
                return redirect('home')
            else:
                return render(request, 'register.html', context = {'form': form})
        data = {'form': form}
        return render(request, 'register.html', context = data)
    else:
        return redirect('login')

@login_required
@user_passes_test(lambda u: u.is_staff)
def register_vendor(request):
    if request.user.groups.filter(name='Admin').exists():
        form = UserRegistrationForm()
        if request.method == 'POST':
            vendorGroup = Group.objects.get(name='Vendor')
            password = request.POST.get('password')
            newpassword = make_password(password)
            data = request.POST.copy()
            data['password'] = newpassword
            form = UserRegistrationForm(data)
            if form.is_valid():
                user = form.save()
                user.groups.add(vendorGroup)
                user.save()
                return redirect('home')
            else:
                return render(request, 'register.html', context = {'form': form})
        data = {'form': form}
        return render(request, 'register.html', context = data)
    else:
        return redirect('login')

@login_required
@user_passes_test(lambda u: u.is_staff)
def register_admin(request):
    if request.user.groups.filter(name='Admin').exists():
        form = UserRegistrationForm()
        if request.method == 'POST':
            adminGroup = Group.objects.get(name='Admin')
            password = request.POST.get('password')
            newpassword = make_password(password)
            data = request.POST.copy()
            data['password'] = newpassword
            form = UserRegistrationForm(data)
            if form.is_valid():
                user = form.save()
                user.groups.add(adminGroup)
                user.is_superuser = True
                user.is_staff = True
                user.save()
                return redirect('home')
            else:
                return render(request, 'register.html', context = {'form': form})
        data = {'form': form}
        return render(request, 'register.html', context = data)
    else:
        return redirect('login')
    
def is_Admin(user):
    return user.groups.filter(name='Admin').exists()

def is_EventPlanner(user):
    return user.groups.filter(name='Event Planner').exists()

def is_Vendor(user):
    return user.groups.filter(name='Vendor').exists()

def is_Client(user):
    return user.groups.filter(name='Client').exists()

def userLogin(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user == None:
            data = {'form': form, 'error': 'Invalid username or password'}
            return render(request, 'login.html', context = data)
        else:
            login(request, user)
            return redirect('home')
    data = {'form': form}
    return render(request, 'login.html', context = data)

def resetPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate token
            token = get_random_string(length=32)
            # Store token and expiry in session
            request.session['reset_token'] = token
            request.session['reset_email'] = email
            request.session['reset_expiry'] = (
                datetime.datetime.now() + datetime.timedelta(hours=24)
            ).isoformat()
            
            # Send reset email
            reset_link = f"{settings.SITE_URL}/password-reset-confirm/{token}/"
            email_subject = 'Password Reset Request'
            email_message = f'''
            Hello {user.username},
            
            You have requested to reset your password. Please click the following link to set a new password:
            
            {reset_link}
            
            This link will expire in 24 hours.
            
            If you did not request this password reset, please ignore this email.
            
            Best regards,
            Your Application Team
            '''
            
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(
                request,
                'Password reset instructions have been sent to your email.'
            )
            return render(request, 'password_reset.html')
        except User.DoesNotExist:
            messages.error(
                request,
                'No account found with that email address.'
            )
    return render(request, 'password_reset.html')

def resetPasswordConfirm(request, token):
    stored_token = request.session.get('reset_token')
    stored_email = request.session.get('reset_email')
    expiry = request.session.get('reset_expiry')
    
    # Validate token and expiry
    if not all([stored_token, stored_email, expiry]):
        messages.error(request, 'Invalid password reset link.')
        return redirect('login')
    
    if stored_token != token:
        messages.error(request, 'Invalid password reset token.')
        return redirect('login')
    
    if datetime.datetime.now() > datetime.datetime.fromisoformat(expiry):
        messages.error(request, 'Password reset link has expired.')
        return redirect('login')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'password_reset_confirm.html')
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'password_reset_confirm.html')
        
        try:
            user = User.objects.get(email=stored_email)
            user.password = make_password(password)
            user.save()
            
            # Clear session data
            del request.session['reset_token']
            del request.session['reset_email']
            del request.session['reset_expiry']
            
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('login')
    return render(request, 'password_reset_confirm.html')

def userlogout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
@user_passes_test(lambda u: is_Admin(u) or is_EventPlanner(u))
def eventCreation(request):
    form = EventCreationForm()
    if request.method == 'POST':
        form = EventCreationForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('event-details', pk=event.pk)
        else:
            return render(request, 'eventCreation.html', context = {'form': form})
    data = {'form': form}
    return render(request, 'eventCreation.html', context = data)

class EventDetailView(DetailView):
    model = Event
    template_name = 'eventDetails.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        
        if self.request.user.is_authenticated:
            context['is_user_registered'] = EventRegistration.objects.filter(
                event=event,
                client=self.request.user
            ).exists()
            vendor_assignment = VendorAssignment.objects.filter(event=event).first()
            context['assigned_vendors'] = vendor_assignment.vendor.name if vendor_assignment else ''
        else:
            context['is_user_registered'] = False
            context['assigned_vendors'] = ''
            
        return context

class EventFilter(django_filters.FilterSet):
    categories = django_filters.ModelMultipleChoiceFilter(
        queryset=EventCategory.objects.all(),
        label="Categories",
        required=False,
        method='filter_categories'
    )
    date = django_filters.DateFilter(field_name='date', lookup_expr='date')  # If date is DateTimeField
    location = django_filters.CharFilter(lookup_expr='icontains')
    vip_cost = django_filters.NumberFilter(lookup_expr='lte')  # Example: filter events where VIP cost <= value
    standard_cost = django_filters.NumberFilter(lookup_expr='lte')
    
    def filter_categories(self, queryset, name, value):
        if value:
            return queryset.filter(categories__in=value)
        return queryset
    
    class Meta:
        model = Event
        fields = ['categories', 'date', 'location', 'vip_cost', 'standard_cost']


class EventListView(FilterView):
    model = Event
    template_name = 'eventList.html'
    context_object_name = 'events'
    filterset_class = EventFilter
    
    def get_queryset(self):
        queryset = Event.objects.all()
        search_query = self.request.GET.get('search', '')
        
        if search_query:
            queryset = Event.objects.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(location__icontains=search_query)
            ).distinct()
            return queryset
            
        if is_Admin(self.request.user) or is_Client(self.request.user) or is_Vendor(self.request.user):
            return queryset
        else:
            return Event.objects.all()

@login_required(login_url='login')
@user_passes_test(lambda u: is_Admin(u) or is_EventPlanner(u))
def eventUpdate(request, pk):
    event_obj = Event.objects.get(id=pk)
    if request.method == 'POST':
        form = EventCreationForm(request.POST, instance=event_obj)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('event-details', pk=pk)  # Use the pk parameter instead of form.pk
        else:
            return render(request, 'eventUpdate.html', context = {'form': form})
    form = EventCreationForm(instance=event_obj)
    data = {'form': form}
    return render(request, 'eventUpdate.html', context = data)

@login_required(login_url='login')
@user_passes_test(lambda u: is_Admin(u) or is_EventPlanner(u))
def eventDelete(request, pk):
    event_obj = Event.objects.get(id=pk)
    event_obj.delete()
    return redirect('home')

@login_required(login_url='login')
@user_passes_test(lambda u: is_Admin(u) or is_Vendor(u))
def create_vendor_profile(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            selected_categories = form.cleaned_data.get('categories')
            vendor.categories.set(selected_categories)
            vendor.user = request.user
            vendor.save()
            return redirect('vendor-details', pk=vendor.pk)
    else:
        form = VendorForm()
    return render(request, 'vendorCreate.html', {'form': form})

@login_required(login_url='login')
@user_passes_test(lambda u: is_Admin(u) or is_Vendor(u))
def update_vendor_profile(request, pk):
    vendor = Vendor.objects.get(pk=pk)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            vendor = form.save(commit=False)
            selected_categories = form.cleaned_data.get('categories')
            vendor.categories.set(selected_categories)
            vendor.user = request.user
            vendor.save()
            return redirect('vendor-details', pk=vendor.pk)
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'vendorUpdate.html', {'form': form})

def delete_vendor(request, pk):
    vendor = Vendor.objects.get(pk=pk)
    vendor.delete()
    return redirect('vendor-list')

class VendorDetailView(DetailView):
    model = Vendor
    template_name = 'vendorDetails.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor = self.get_object()
        feedbacks = VendorFeedback.objects.filter(vendor=vendor)
        total = sum(feedback.rating for feedback in feedbacks)
        context['aggregated_rating'] = total / feedbacks.count() if feedbacks.count() > 0 else 0
        return context

class VendorListView(ListView):
    model = Vendor
    template_name = 'vendorList.html'
    context_object_name = 'vendor'

@login_required(login_url='login')  
@user_passes_test(lambda u: is_Admin(u) or is_EventPlanner(u))
def assign_vendor(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    available_vendors = Vendor.objects.filter(is_available=True)

    if request.method == 'POST':
        form = VendorAssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.event = event
            assignment.vendor = form.cleaned_data['vendor']
            
            vendor = assignment.vendor
            vendor.is_available = False
            vendor.save()
            
            assignment.save()
            return redirect('assign-vendors', pk=event.id)
    else:
        form = VendorAssignmentForm()
        # Limit vendor choices to only available vendors
        form.fields['vendor'].queryset = available_vendors

    data = {
        'form': form, 
        'event': event, 
        'available_vendors': available_vendors
    }
    return render(request, 'vendorAssignment.html', context=data)
    
def vendor_assigned_events(request,vendor_id):
    if VendorAssignment.objects.filter(vendor_id=vendor_id).exists():
        vendor = get_object_or_404(Vendor, id=vendor_id)
        assignments = VendorAssignment.objects.filter(vendor=vendor).select_related('event')
        return render(request, 'vendorAssignedEvents.html', {'assignments': assignments, 'vendor': vendor})
    else:
        return render(request, 'vendorAssignedEvents.html', {'assignments': []})

def get_available_vendors(request):
    available_assignments = VendorAssignment.objects.filter(vendor__is_available=True)
    available_assignments = VendorAssignment.objects.filter(
        vendor__is_available=True,
        is_confirmed=True  # If you want only confirmed assignments
    )
    available_vendors = Vendor.objects.filter(is_available=True)

@login_required(login_url='login')
@user_passes_test(lambda u: is_Admin(u) or is_Vendor(u))
def update_vendor_availability(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    vendor.is_available = not vendor.is_available
    vendor.save()
    return redirect('vendor-details', pk=vendor_id)

@login_required(login_url='login')
def userProfile(request):
    user = request.user
    registered_events = EventRegistration.objects.filter(client=request.user)
    my_tickets = Ticket.objects.filter(
        event__in=registered_events.values_list('event', flat=True)
    ).select_related('event', 'ticket_type')
    
    # For admin users
    if request.user.is_staff:
        all_invoices = Invoice.objects.all().select_related('event', 'client')
    else:
        all_invoices = None
        
    # For event planners
    if request.user.groups.filter(name='EventPlanner').exists():
        planner_invoices = Invoice.objects.filter(event__created_by=request.user)
    else:
        planner_invoices = None
        
    context = {
        'user': user,
        'my_tickets': my_tickets,
        'all_invoices': all_invoices,
        'planner_invoices': planner_invoices
    }
    
    return render(request, 'userProfile.html', context)

@login_required(login_url='login')
def editProfile(request):
    user = request.user
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile')
    else:
        form = UserForm(instance=user)
    return render(request, 'editProfile.html', {'form': form})

@login_required(login_url='login')
def eventRegister(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Validate event capacity
    if event.max_attendees and event.registrations >= event.max_attendees:
        messages.error(request, 'Sorry, this event has reached maximum capacity.')
        return redirect('event-details', pk=event.id)
    
    # Check existing registration
    if EventRegistration.objects.filter(event=event, client=request.user).exists():
        messages.info(request, 'You are already registered for this event.')
        return redirect('event-details', pk=event.id)
        
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create registration
                registration = form.save(commit=False)
                registration.event = event
                registration.client = request.user
                registration.registration_date = timezone.now()
                registration.save()
                
                # Update event count
                event.registrations += 1
                event.save()
                
                # Get selected ticket type and create ticket
                ticket_type = form.cleaned_data['ticket_type']
                ticket_price = {
                    'Attendee': 0,
                    'General Admission': 500, 
                    'VIP': 2000
                }.get(ticket_type.name, 0)
                
                Ticket.objects.create(
                    ticket_type=ticket_type,
                    event=event,
                    price=ticket_price,
                    is_valid=True
                )
                return redirect('ticket-purchase', event_id=event.id)
        
        return render(request, 'eventRegistration.html', {'form': form, 'event': event})
        
    form = EventRegistrationForm(initial={'client': request.user})
    context = {
        'form': form,
        'event': event,
        'remaining_spots': event.max_attendees - event.registrations if event.max_attendees else None
    }
    return render(request, 'eventRegistration.html', context)

@login_required
def ticket_purchase(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # Get the user's registration for this event
    registration = get_object_or_404(EventRegistration, event=event, client=request.user)
    
    if request.method == 'POST':
        # Use the ticket type from registration
        ticket_type = registration.ticket_type
        quantity = 1  # Since it's linked to registration, quantity is 1
        
        # Get price based on ticket type
        price = {
            'Attendee': 0,
            'General Admission': 500, 
            'VIP': 2000
        }.get(ticket_type.name, 0)
                
        # Create invoice only for paid ticket types
        if ticket_type.name in ['VIP', 'General Admission']:
            invoice = Invoice.objects.create(
                client=request.user,
                event=event,
                total_amount=price * quantity,
                invoice_date=timezone.now(),
                payment_status='Pending'
            )
            
        # Create ticket using registration's ticket type
        ticket = Ticket.objects.create(
            ticket_type=ticket_type,
            event=event,
            price=price,
            is_valid=True
        )
        return redirect('download-ticket', ticket_id=ticket.id)
    
    return render(request, 'ticketPurchase.html', {
        'event': event,
        'selected_ticket_type': registration.ticket_type
    })
    
@login_required(login_url='login')
def cancelTicket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, event__eventregistration__client=request.user)
    
    if request.method == 'POST':
        ticket.is_valid = False
        ticket.save()
        return redirect('user-profile')
    
    return render(request, 'cancelTicket.html', {'ticket': ticket})

    
@login_required
def eventUnregister(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    try:
        with transaction.atomic():
            registration = get_object_or_404(EventRegistration, event=event, client=request.user)
            registration.delete()
            
            # Update event registration count
            event.registrations = max(0, event.registrations - 1)
            event.save()
            
            messages.success(request, 'Successfully unregistered from the event.')
    except Exception as e:
        messages.error(request, 'Error unregistering from event.')
        
    return redirect('event-details', pk=event.id)

@login_required(login_url='login')
def registeredStatus(request, event_id):
    event = get_object_or_404(Event.objects.select_related('category'), id=event_id)
    registrations = EventRegistration.objects.filter(event=event).select_related('client').order_by('-registration_date')
    
    context = {
        'event': event,
        'registrations': registrations,
        'total_registrations': registrations.count(),
        'is_user_registered': EventRegistration.objects.filter(event=event, client=request.user).exists(),
        'remaining_spots': event.max_attendees - registrations.count() if event.max_attendees else None
    }
    return render(request, 'eventDetails.html', context)

@login_required(login_url='login')
@user_passes_test(lambda u: is_Admin(u) or is_EventPlanner(u))
def event_registration_list(request):
    if is_Admin(request.user):
        # Admin sees all registrations
        registrations = EventRegistration.objects.all()
    else:
        # Event planner sees registrations only for their events
        registrations = EventRegistration.objects.filter(event__created_by=request.user)
    
    return render(request, 'eventRegistrationList.html', {'registrations': registrations})

@login_required(login_url='login')
@user_passes_test(lambda u: is_Admin(u) or is_EventPlanner(u))    
def logistics_management(request, event_id):
    event = Event.objects.get(id=event_id)
    logistics = Logistics.objects.filter(event=event)
    if request.method == 'POST':
        form = LogisticsForm(request.POST)
        if form.is_valid():
            logistic = form.save(commit=False)
            logistic.event = event
            logistic.save()
            return redirect('logistics', event_id=event_id)
    else:
        form = LogisticsForm()
    return render(request, 'logisticsManagement.html', {'event': event, 'logistics': logistics, 'form': form})

@login_required(login_url='login')
@user_passes_test(lambda u: is_Admin(u) or is_EventPlanner(u))
def logistics_delete(request, logistics_id):
    logistics = get_object_or_404(Logistics, id=logistics_id)
    event_id = logistics.event.id
    logistics.delete()
    return redirect('logistics', event_id=event_id)

@login_required(login_url='login')
@user_passes_test(lambda u: is_Admin(u) or is_EventPlanner(u))
def inventory_tracking(request, event_id):
    event = Event.objects.get(id=event_id)
    inventory = Inventory.objects.filter(event=event)
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.event = event
            item.save()
            return redirect('inventory', event_id=event_id)
    else:
        form = InventoryForm()
    return render(request, 'inventoryTracking.html', {'event': event, 'inventory': inventory, 'form': form})

@login_required(login_url='login')
@user_passes_test(lambda u: is_Admin(u) or is_EventPlanner(u))
def inventory_delete(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)
    event_id = inventory.event.id
    inventory.delete()
    return redirect('inventory', event_id=event_id)

def give_event_reviews(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reviews = EventReview.objects.filter(event=event)
    if request.method == 'POST':
        form = EventReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.event = event
            review.save()
            return redirect('event-details', pk=event_id)
    else:
        form = EventReviewForm()
    return render(request, 'eventReview.html', {'event': event, 'reviews': reviews, 'form': form})

@login_required(login_url='login')
@user_passes_test(lambda u: is_Admin(u))
def approve_reviews(request, review_id):
    review = get_object_or_404(EventReview, id=review_id)
    review.is_approved = True
    review.save()
    return redirect('event-details', pk=review.event.id)
    # return redirect('event-reviews', event_id=review.event.id)

def event_reviews(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reviews = EventReview.objects.filter(event=event)
    return render(request, 'eventReviewList.html', {'event': event, 'reviews': reviews})

@login_required(login_url='login')
@user_passes_test(lambda u: is_Admin(u))
def review_delete(request, review_id):
    review = get_object_or_404(EventReview, id=review_id)
    event_id = review.event.id
    review.delete()
    return redirect('event-reviews', event_id=event_id)

def view_your_reviews(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reviews = EventReview.objects.filter(event=event, user=request.user)
    return render(request, 'yourReviews.html', {'event': event, 'reviews': reviews})

def feedback_for_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    feedbacks = VendorFeedback.objects.filter(vendor=vendor)
    if request.method == 'POST':
        form = VendorFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.vendor = vendor
            feedback.save()
            return redirect('vendor-details', pk=vendor_id)
    else:
        form = VendorFeedbackForm()
    return render(request, 'feedbackForVendor.html', {'vendor': vendor, 'feedbacks': feedbacks, 'form': form})

def view_all_feedbacks(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    feedbacks = VendorFeedback.objects.filter(vendor=vendor)
    return render(request, 'allFeedbacks.html', {'vendor': vendor, 'feedbacks': feedbacks})

@login_required(login_url='login')
def download_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Generate ticket PDF using the ticket details
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.unique_code}.pdf"'
    
    # Create PDF
    p = canvas.Canvas(response)
    p.drawString(100, 800, f"Event: {ticket.event.name}")
    p.drawString(100, 780, f"Ticket Type: {ticket.ticket_type.name}")
    p.drawString(100, 760, f"Ticket Code: {ticket.unique_code}")
    p.drawString(100, 740, f"Date: {ticket.event.date}")
    p.drawString(100, 720, f"Venue: {ticket.event.location}")
    p.drawString(100, 700, f"Ticket Validity(True or False): {ticket.is_valid}")
    p.save()
    
    return response

@login_required(login_url='login')
def download_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.pdf"'
    
    p = canvas.Canvas(response)
    p.drawString(100, 800, f"Invoice: {invoice.id}")
    p.drawString(100, 780, f"Event: {invoice.event.name}")
    p.drawString(100, 760, f"Amount: ${invoice.total_amount}")
    p.drawString(100, 740, f"Date: {invoice.invoice_date}")
    p.drawString(100, 720, f"Status: {invoice.payment_status}")
    p.save()
    
    return response

class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoiceDetail.html'
    context_object_name = 'invoice'
    
def changePassword(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data.get('password')
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')
            
            # First validate that new passwords match
            if new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
                return render(request, 'changePassword.html', {'form': form})
            
            # Then check if old password is correct
            if not user.check_password(old_password):
                messages.error(request, 'Current password is incorrect.')
                return render(request, 'changePassword.html', {'form': form})
            
            # Basic password validation
            if len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return render(request, 'changePassword.html', {'form': form})
            
            # If all validations pass, change the password
            user.set_password(new_password)
            user.save()
            
            # Keep the user logged in
            update_session_auth_hash(request, user)
            
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user-profile')  # Assuming your profile URL name is 'user-profile'
    else:
        form = ChangePasswordForm()
    
    return render(request, 'changePassword.html', {'form': form})

@login_required(login_url='login')
@user_passes_test(lambda u: is_Admin(u))
def changeInvoiceStatus(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    # Define status cycle order
    status_cycle = ['Pending', 'Paid', 'Cancelled']
    current_index = status_cycle.index(invoice.payment_status)
    next_index = (current_index + 1) % len(status_cycle)
    
    # Update to next status in cycle
    invoice.payment_status = status_cycle[next_index]
    invoice.save()
    return redirect('invoice-detail', pk=invoice.id)

def attendance_report(request, event_id):
    event = Event.objects.get(id=event_id)
    tickets = Ticket.objects.filter(event=event).count()
    attendees_present = Ticket.objects.filter(event=event, is_valid=True).count()
    
    context = {
        'event': event,
        'tickets': tickets,
        'attendees_present': attendees_present,
    }
    return render(request, 'attendanceReport.html', context)

def revenue_report(request, event_id):
    event = Event.objects.get(id=event_id)
    ticket_revenue = Ticket.objects.filter(event=event).aggregate(Sum('price'))['price__sum'] or 0
    vendor_fees = Invoice.objects.filter(event=event).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    context = {
        'event': event,
        'ticket_revenue': ticket_revenue,
        'vendor_fees': vendor_fees,
        'total_revenue': ticket_revenue + vendor_fees,
    }
    return render(request, 'revenueReport.html', context)

def analytics_dashboard(request):
    user = request.user
    context = {'role': 'Guest'}  # Default context for non-authenticated users

    if user.groups.filter(name='Client').exists():
        registered_events = Event.objects.filter(eventregistration__client=user)
        upcoming_events = registered_events.filter(date__gte=timezone.now()).order_by('date')

        context = {
            'role': 'Client',
            'registered_events': registered_events,
            'upcoming_events': upcoming_events,
        }

    elif user.groups.filter(name='EventPlanner').exists():
        created_events = Event.objects.filter(created_by=user).order_by('date')
        total_revenue = Invoice.objects.filter(event__in=created_events).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_tickets = Ticket.objects.filter(event__in=created_events).count()

        context = {
            'role': 'EventPlanner',
            'created_events': created_events,
            'total_revenue': total_revenue,
            'total_tickets': total_tickets,
        }

    elif user.groups.filter(name='Vendor').exists():
        all_vendors = Vendor.objects.all()
        total_feedbacks = VendorFeedback.objects.filter(vendor__in=all_vendors).count()
        total_performance = VendorPerformance.objects.filter(vendor__in=all_vendors).count()
        
        context = {
            'role': 'Vendor',
            'total_feedbacks': total_feedbacks,
            'total_performance': total_performance,
            'all_vendors': all_vendors,
        }
        
    
    elif user.is_staff:
        all_events = Event.objects.all().order_by('date')
        total_revenue = Invoice.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_tickets = Ticket.objects.aggregate(Count('id'))['id__count'] or 0

        context = {
            'role': 'Admin',
            'all_events': all_events,
            'total_revenue': total_revenue,
            'total_tickets': total_tickets,
        }

    return render(request, 'home.html', context)