from django.contrib import admin
from django.urls import path
from flats import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.owner_login, name="owner_login"),
    path("home/", views.owner_home, name="owner_home"),
    path("payments/", views.owner_payments, name="owner_payments"),
    path("receipt/<int:payment_id>/", views.owner_receipt, name="owner_receipt"),
    path("announcements/", views.owner_announcements, name="owner_announcements"),
    path("message/", views.owner_message, name="owner_message"),
    path("logout/", views.owner_logout, name="owner_logout"),
]