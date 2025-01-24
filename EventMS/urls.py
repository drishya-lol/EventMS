"""
URL configuration for EventMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from base.views import userRegistration, home, userLogin, userlogout, ResetPasswordView, eventCreation, EventDetailView, EventListView, eventUpdate, eventDelete, search_events, create_vendor_profile, update_vendor_profile, VendorDetailView, VendorListView, assign_vendor, vendor_assigned_events, update_vendor_availability, userProfile, editProfile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', userRegistration, name = 'register'),
    path('login/', userLogin, name = 'login'),
    path('logout/', userlogout, name = 'logout'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('event-create/', eventCreation, name='event-create'),
    path('event-list/', EventListView.as_view(), name='event-list'),
    path('event-details/<int:pk>/', EventDetailView.as_view(), name='event-details'),
    path('event-update/<int:pk>/', eventUpdate, name='event-update'),
    path('event-delete/<int:pk>/', eventDelete, name='event-delete'),
    path('search/', search_events, name='search_events'),
    path('vendor-create/', create_vendor_profile, name='vendor-create'),
    path('vendor-update/<int:pk>/', update_vendor_profile, name='vendor-update'),
    path('vendor-details/<int:pk>/', VendorDetailView.as_view(), name='vendor-details'),
    path('vendor-list/', VendorListView.as_view(), name='vendor-list'),
    path('assign-vendor/<int:event_id>/', assign_vendor, name='assign_vendor'),
    path('vendor-assigned-events/<int:vendor_id>/', vendor_assigned_events, name='vendor-assigned-events'),
    path('update-vendor-availability/<int:assignment_id>/', update_vendor_availability, name='update-vendor-availability'),
    path('user-profile/', userProfile, name='user-profile'),
    path('edit-profile/', editProfile, name='edit-profile'),
]
