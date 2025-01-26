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
from base import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.userRegistration, name = 'register'),
    path('login/', views.userLogin, name = 'login'),
    path('logout/', views.userlogout, name = 'logout'),
    path('event-create/', views.eventCreation, name='event-create'),
    path('event-list/', views.EventListView.as_view(), name='event-list'),
    path('event-details/<int:pk>/', views.EventDetailView.as_view(), name='event-details'),
    path('event-update/<int:pk>/', views.eventUpdate, name='event-update'),
    path('event-delete/<int:pk>/', views.eventDelete, name='event-delete'),
    path('vendor-create/', views.create_vendor_profile, name='vendor-create'),
    path('vendor-update/<int:pk>/', views.update_vendor_profile, name='vendor-update'),
    path('vendor-details/<int:pk>/', views.VendorDetailView.as_view(), name='vendor-details'),
    path('vendor-list/', views.VendorListView.as_view(), name='vendor-list'),
    path('vendor-delete/<int:pk>/', views.delete_vendor, name='vendor-delete'),
    path('assign-vendor/<int:event_id>/', views.assign_vendor, name='assign-vendor'),
    path('vendor-assigned-events/<int:vendor_id>/', views.vendor_assigned_events, name='vendor-assigned-events'),
    path('update-vendor-availability/<int:vendor_id>/', views.update_vendor_availability, name='update-vendor-availability'),
    path('user-profile/', views.userProfile, name='user-profile'),
    path('edit-profile/', views.editProfile, name='edit-profile'),
    path('register-event-planner/', views.register_eventPlanner, name='register-event-planner'),
    path('register-vendor/', views.register_vendor, name='register-vendor'),
    path('register-admin/', views.register_admin, name='register-admin'),
    path('event-details/<int:event_id>/register/', views.eventRegister, name='event-register'),
    path('event-details/<int:event_id>/unregister/', views.eventUnregister, name='event-unregister'),
    path('event-registration-list/', views.event_registration_list, name='event-registration-list'),
    path('ticket-purchase/<int:event_id>/', views.ticket_purchase, name='ticket-purchase'),
    path('invoice/<int:invoice_id>/', views.InvoiceDetailView.as_view(), name='invoice-detail'),
    path('event-details/<int:event_id>/status/', views.registeredStatus, name='registered-status'),
    path('logistics/<int:event_id>/', views.logistics_management, name='logistics'),
    path('logistics/<int:logistics_id>/delete/', views.logistics_delete, name='logistics-delete'),
    path('inventory/<int:event_id>/', views.inventory_tracking, name='inventory'),
    path('inventory/<int:inventory_id>/delete/', views.inventory_delete, name='inventory-delete'),
    path('event-details/<int:event_id>/reviews/', views.give_event_reviews, name='give-event-reviews'),
    path('event-reviews/<int:event_id>/', views.event_reviews, name='event-reviews'),
    path('approve-reviews/<int:review_id>', views.approve_reviews, name='approve-reviews'),
    path('review/<int:review_id>/delete/', views.review_delete, name='review-delete'),
    path('view-your-reviews/<int:event_id>', views.view_your_reviews, name='view-your-reviews'),
    path('feedback-for-vendor/<int:vendor_id>', views.feedback_for_vendor, name='vendor-feedback'),
    path('view-all-feedbacks/<int:vendor_id>', views.view_all_feedbacks, name='view-all-feedbacks'),
    path('ticket/<int:ticket_id>/download/', views.download_ticket, name='download-ticket'),
]
