from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm, EventCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Event, EventCategory, EventRegistration, Vendor, VendorCategory, VendorPerformance, Ticket
from django.views.generic import DetailView, ListView
from django.contrib.auth.models import Group
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

def eventUpdate(request, pk):
    event_obj = Event.objects.get(id=pk)
    if request.method == 'POST':
        form = EventCreationForm(request.POST, instance=event_obj)
        if form.is_valid():
            form.save()
            return redirect('event-details', pk=form.pk)
        else:
            return render(request, 'eventUpdate.html', context = {'form': form})
    form = EventCreationForm(instance=event_obj)
    data = {'form': form}
    return render(request, 'eventUpdate.html', context = data)

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
