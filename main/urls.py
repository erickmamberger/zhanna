from django.urls import path
from main.views import CoreView, ContactsView, PayView, GetTicketView, history  # , test  # , pay_check

urlpatterns = [
    path('', CoreView.as_view(), name='home'),
    path('tickets/', GetTicketView.as_view(), name='get_ticket'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('payment/', PayView.as_view(), name='pay'),
    path('check/', history),
    # path('payment/<str:id>/', pay_check, name='pay_check'),

]