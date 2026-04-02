from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='owner_home'),
    path('payments/', views.payments_page, name='owner_payments'),
    path('announcements/', views.announcements_page, name='owner_announcements'),
    path('message/', views.messages_page, name='owner_message'),
    path('receipt/', views.receipt_page, name='owner_receipt_page'),

    # optional admin-style pages if you still use them
    path('flat-infos/', views.flat_infos_page, name='flat_infos'),
    path('houses/', views.houses_page, name='houses'),
]