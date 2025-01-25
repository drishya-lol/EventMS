from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, LoginForm, EventCreationForm, VendorForm, VendorAssignmentForm, UserForm, EventRegistrationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Event, EventCategory, EventRegistration, Vendor, VendorCategory, VendorPerformance, Ticket, VendorAssignment
from django.views.generic import DetailView, ListView
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib import messages
from django.utils import timezone

# Create your views here.

def home(request):
    return render(request, 'home.html')

def userRegistration(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        password = request.POST.get('password')
        newpassword = make_password(password)
        data = request.POST.copy()
        data['password'] = newpassword
        form = UserRegistrationForm(data)
        if form.is_valid():
            form.save()
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
                return redirect('login')
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
                return redirect('login')
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
                return redirect('login')
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
    context_object_name = 'event'

class EventListView(ListView):
    model = Event
    template_name = 'eventList.html'
    context_object_name = 'events'

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

def search_events(request):
    query = request.GET.get('query', '').strip()
    category = request.GET.get('category', '')
    date = request.GET.get('date', '')
    location = request.GET.get('location', '').strip()
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    
    events = Event.objects.all()
    
    # Enhanced search with Q objects for more flexible querying
    if query:
        from django.db.models import Q
        events = events.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(organizer__icontains=query)
        )
    
    if category:
        events = events.filter(category__name=category)
    
    if date:
        from datetime import datetime
        try:
            search_date = datetime.strptime(date, '%Y-%m-%d').date()
            events = events.filter(date=search_date)
        except ValueError:
            pass
    
    if location:
        events = events.filter(
            Q(location__icontains=location) |
            Q(venue__icontains=location)
        )
    
    # Price range filtering
    if price_min:
        events = events.filter(price__gte=float(price_min))
    if price_max:
        events = events.filter(price__lte=float(price_max))
    
    # Order results by date and name
    events = events.order_by('date', 'name')

    context = {
        'events': events,
        'query': query,
        'category': category,
        'date': date,
        'location': location,
        'price_min': price_min,
        'price_max': price_max,
        'categories': EventCategory.objects.all()
    }
    
    return render(request, 'search_results.html', context)

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
    
    # Check if user already registered
    if EventRegistration.objects.filter(event=event, client=request.user).exists():
        return redirect('event-details', pk=event.id)
        
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.client = request.user
            registration.registration_date = timezone.now()

            # Check event capacity
            if event.max_attendees and event.registrations.count() >= event.max_attendees:
                messages.error(request, 'Sorry, this event has reached maximum capacity.')
                return redirect('event-details', pk=event.id)
                
            registration.save()
            messages.success(request, 'Successfully registered for the event!')
            return redirect('event-details', pk=event.id)
    else:
        form = EventRegistrationForm(initial={'client': request.user})
        
    context = {
        'form': form,
        'event': event,
        'remaining_spots': event.max_attendees - event.eventregistration_set.count() if event.max_attendees else None
    }
    return render(request, 'eventRegistration.html', context)

@login_required(login_url='login')
def registeredStatus(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registrations = event.registrations.select_related('user').order_by('-registration_date')
    
    context = {
        'event': event,
        'registrations': registrations,
        'total_registrations': registrations.count(),
        'is_user_registered': registrations.filter(user=request.user).exists(),
    }
    return render(request, 'eventDetails.html', context)