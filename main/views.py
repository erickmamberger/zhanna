from datetime import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from main.service import mailing
from main.models import Tickets
from django.views.generic import TemplateView


class CoreView(TemplateView):
    template_name = 'main/index.html'


class ContactsView(TemplateView):
    template_name = 'main/contacts.html'


class GetTicketView(TemplateView):
    template_name = 'main/get_ticket.html'

    def get(self, request):
        queryset = Tickets.objects.filter(is_published=True, time__gte=datetime.now())
        return render(request, 'main/get_ticket.html', {"tickets": queryset})

    # добавить валидацию. в целом все ок. предусмотреть все возможные исключения
    def post(self, request):
        try:
            target_ticket = Tickets.objects.get(str_date=request.POST['time'], is_published=True)
        except:
            messages.error(request, 'Занять слот или нужно проверить правильность введенной формы')
            queryset = Tickets.objects.filter(is_published=True, time__gte=datetime.now())
            return render(request, 'main/get_ticket.html', {"tickets": queryset})

        target_ticket.is_published = False
        target_ticket.save()

        mailing(time=request.POST['time'], target_email=request.POST['email'], target_phone=request.POST['phone'])

        messages.success(request, 'Вы успешно записались на консультацию!')
        request.session["custom_signal"] = 1
        return redirect('home')


class QrView(TemplateView):
    template_name = 'main/qr.html'