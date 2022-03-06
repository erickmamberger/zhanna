from django.urls import path
from main.views import CoreView, ContactsView, GetTicketView, QrView

urlpatterns = [
    path('', CoreView.as_view(), name='home'),
    path('tickets/', GetTicketView.as_view(), name='get_ticket'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('qr/', QrView.as_view(), name='qr'),

]