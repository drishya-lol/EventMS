from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, LoginForm, EventCreationForm, VendorForm, VendorAssignmentForm, UserForm, EventRegistrationForm, LogisticsForm, InventoryForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Event, EventCategory, EventRegistration, Vendor, VendorCategory, VendorPerformance, Ticket, VendorAssignment, TicketType, Invoice, Logistics, Inventory
from django.views.generic import DetailView, ListView
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib import messages
from django.utils import timezone
from django.db import transaction

# Create your views here.

def home(request):
    return render(request, 'home.html')

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
    pass

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
            event = form.save()
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
        context['is_user_registered'] = EventRegistration.objects.filter(
            event=event, 
            client=self.request.user
        ).exists()
        return context

class EventListView(ListView):
    model = Event
    template_name = 'eventList.html'
    context_object_name = 'events'
    filterset_fields = ['category', 'date', 'location', 'price']
    search_fields = ['name', 'description']
    def get_queryset(self):
        if is_Admin(self.request.user) or is_Client(self.request.user):
            return Event.objects.all()
        else:
            return Event.objects.filter(created_by=self.request.user)

@login_required(login_url='login')
@user_passes_test(lambda u: is_Admin(u) or is_EventPlanner(u))
def eventUpdate(request, pk):
    event_obj = Event.objects.get(id=pk)
    if request.method == 'POST':
        form = EventCreationForm(request.POST, instance=event_obj)
        if form.is_valid():
            form.save()
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
            form.save()
            return redirect('vendor-list')
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'vendorUpdate.html', {'form': form})

class VendorDetailView(DetailView):
    model = Vendor
    template_name = 'vendorDetails.html'
    context_object_name = 'vendor'

class VendorListView(ListView):
    model = Vendor
    template_name = 'vendorList.html'
    context_object_name = 'vendor'

@login_required(login_url='login')  
@user_passes_test(lambda u: is_Admin(u) or is_EventPlanner(u))
def assign_vendor(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = VendorAssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.event = event
            assignment.save()
            return redirect('event-details', pk=event.id)
    else:
        form = VendorAssignmentForm()
    
    data = {'form': form, 'event': event}
    return render(request, 'vendorAssignment.html', context=data)

def vendor_assigned_events(request,vendor_id):
    vendor = get_object_or_404(VendorAssignment, id=vendor_id)
    assignments = vendor.assignments.select_related('event').all()
    return render(request, 'vendorAssignedEvents.html', {'assignments': assignments})

@login_required(login_url='login')
@user_passes_test(lambda u: is_Admin(u) or is_Vendor(u))
def update_vendor_availability(request, assignment_id):
    assignment = get_object_or_404(VendorAssignment, id=assignment_id)
    if request.method == 'POST':
        assignment.is_available = not assignment.is_available
        assignment.save()
        return redirect('vendor-assigned-events')
    return render(request, 'updateVendorAvailability.html', {'assignment': assignment})

@login_required(login_url='login')
def userProfile(request):
    user, created = User.objects.get_or_create(id=request.user.id)
    data = {'user': user}
    return render(request, 'userProfile.html', context=data)

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
    
    # Check capacity first before processing anything
    if event.max_attendees and event.registrations >= event.max_attendees:
        messages.error(request, 'Sorry, this event has reached maximum capacity.')
        return redirect('event-details', pk=event.id)
    
    # Check if user already registered
    if EventRegistration.objects.filter(event=event, client=request.user).exists():
        messages.info(request, 'You are already registered for this event.')
        return redirect('event-details', pk=event.id)
        
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                registration = form.save(commit=False)
                registration.event = event
                registration.client = request.user
                registration.registration_date = timezone.now()
                registration.save()
                
                # Update event registration count
                event.registrations += 1
                event.save()
            
            messages.success(request, 'Successfully registered for the event!')
            return redirect('event-details', pk=event.id)
    else:
        form = EventRegistrationForm(initial={'client': request.user})
        
    context = {
        'form': form,
        'event': event,
        'remaining_spots': event.max_attendees - event.registrations if event.max_attendees else None
    }
    return render(request, 'eventRegistration.html', context)

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


@login_required
def ticket_purchase(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    ticket_types = TicketType.objects.all()
    if request.method == 'POST':
        ticket_type_id = request.POST.get('ticket_type')
        ticket_type = get_object_or_404(TicketType, id=ticket_type_id)
        quantity = int(request.POST.get('quantity', 1))
        
        total_price = ticket_type.price * quantity
        
        invoice = Invoice.objects.create(
            client = request.user,
            event = event,
            total_amount = total_price,
            invoice_date = timezone.now(),
            payment_status = 'Pending'
        )
        
        for _ in range(quantity):
            Ticket.objects.create(
                invoice=invoice,
                ticket_type=ticket_type,
                event=event,
                price=ticket_type.price,
                is_valid=True,
            )
        
        messages.success(request, f'Successfully purchased {quantity} ticket(s) for {ticket_type.name}.')
        return redirect('invoice-detail', invoice_id=invoice.id)
    
    return render(request, 'ticketPurchase.html', {'event': event, 'ticket_types': ticket_types})

class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoiceDetail.html'
    context_object_name = 'invoice'

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