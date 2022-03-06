from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from main.service import get_actual_tickets, mailing, test_mail
from main.models import Tickets
from main.service import get_pay_link, check_payment
from django.views.generic import TemplateView


def test(request):
    test_mail()
    return render(request, 'main/get_ticket.html', {"tickets": get_actual_tickets()})


def history(request):
    check_payment(1)
    return render(request, 'main/get_ticket.html', {"tickets": get_actual_tickets()})


class CoreView(TemplateView):
    template_name = 'main/index.html'


class ContactsView(TemplateView):
    template_name = 'main/contacts.html'


class PayView(TemplateView):
    template_name = 'main/pay.html'
    # extra_context = {"pay_link": get_pay_link()}


class GetTicketView(TemplateView):
    template_name = 'main/get_ticket.html'

    def get(self, request):
        pay_link = get_pay_link()
        if pay_link == 0:
            messages.info(request, 'Пожалуйста, для записи позвоните нам по номеру +7 (902) 471 71 34.\n'
                                   'Или напишите через эл. почту или соц. сети.')
            return redirect('home')
        else:
            return render(request, 'main/get_ticket.html', {"tickets": get_actual_tickets(),
                                                            "pay_link": pay_link})

    # добавить валидацию. в целом все ок. предусмотреть все возможные исключения
    def post(self, request):
        try:
            target_ticket = Tickets.objects.get(str_date=request.POST['time'], is_published=True)
        except:
            messages.error(request, 'Занять слот или нужно проверить правильность введенной формы')
            return render(request, 'main/get_ticket.html', {"tickets": get_actual_tickets()})

        if check_payment(request.POST['payment_id']):
            pass
        else:
            messages.error(request, 'Неверный код оплаты или оплата не была проведена.')
            return render(request, 'main/get_ticket.html', {"tickets": get_actual_tickets()})

        target_ticket.is_published = False
        target_ticket.save()

        mailing(time=request.POST['time'], target_email=request.POST['email'], target_phone=request.POST['phone'])

        messages.success(request, 'Вы успешно записались на консультацию!')
        request.session["custom_signal"] = 1
        return redirect('home')


