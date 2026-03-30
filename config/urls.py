from django.contrib import admin
from django.urls import path
from flats import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Owner login
    path("", views.owner_login, name="owner_login"),

    # Owner dashboard
    path("home/", views.owner_home, name="owner_home"),

    # Payments
    path("payments/", views.owner_payments, name="owner_payments"),
    path("receipt/<int:payment_id>/", views.owner_receipt, name="owner_receipt"),

    # Announcements
    path("announcements/", views.owner_announcements, name="owner_announcements"),

    # Messages
    path("message/", views.owner_message, name="owner_message"),

    # Maintenance
    path("maintenance/", views.owner_maintenance_list, name="owner_maintenance_list"),
    path("maintenance/new/", views.owner_maintenance_create, name="owner_maintenance_create"),

    # Logout
    path("logout/", views.owner_logout, name="owner_logout"),
]