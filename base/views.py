from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, LoginForm, EventCreationForm, VendorForm, VendorAssignmentForm, UserForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Event, EventCategory, EventRegistration, Vendor, VendorCategory, VendorPerformance, Ticket, VendorAssignment
from django.views.generic import DetailView, ListView
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
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

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')

def userlogout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
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
