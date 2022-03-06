import uuid
from datetime import datetime

from yoomoney import Quickpay, Client
from django.core.mail import send_mail
from main.models import Tickets


def get_pay_link():
    uniq = str(uuid.uuid4().int)
    uniq = uniq[:6]
    try:
        quickpay = Quickpay(
                    receiver="4100116993572215",
                    quickpay_form="shop",
                    targets="Пожалуйста, сохраните номер вашего платежа:"
                            f"\n{uniq}",
                    paymentType="SB",
                    successURL='https://advokat-mamberger.ru/tickets/',
                    sum=3,
                    label=uniq,
                )
        pay_link = quickpay.redirected_url
    except Exception as ex:
        pay_link = 0
    #print(pay_link)
    return pay_link


def check_payment(id):
    token = '4100116993572215.47B230A343F27009F9BFAF3A638EB2EDCA86B371B4B711D3575E48410B373007A35DF2AA5B9778FD86BAA8EFEBBD6892761D2916730D22FFB8D2AEB7C6239F30771CFE1B4BA250D5B0064C6D2958B4A1DD6996BB376CB1B0BBE67F2127F31B13BE4C6DF83A2AD5A26FAB5064CDA0A0A52EC36CA84616F01EB36EE36FAE020B14'
    client = Client(token)
    history = client.operation_history(label=f"{id}")
    # history = client.operation_history()
    print("List of operations:")
    print("Next page starts with: ", history.next_record)
    for operation in history.operations:
        print()
        print("Operation:", operation.operation_id)
        print("\tStatus     -->", operation.status)
        print("\tDatetime   -->", operation.datetime)
        print("\tTitle      -->", operation.title)
        print("\tPattern id -->", operation.pattern_id)
        print("\tDirection  -->", operation.direction)
        print("\tAmount     -->", operation.amount)
        print("\tLabel      -->", operation.label)
        print("\tType       -->", operation.type)

    for operation in history.operations:
        if operation.status == "success":
            return True
    else:
        return False


def get_actual_tickets():
    queryset = Tickets.objects.filter(is_published=True, time__gte=datetime.now())
    tickets = []
    for x in queryset:
        tickets.append(x.str_date)
    return tickets


def mailing(time, target_email, target_phone):
    text = 'Письмо с оповещением успешно отправленно на указанный клиентом email.'
    try:
        send_mail('Запись в адкатский кабинет', f'Здравствуйте!\nВы записаны на консультацию в {time}',
                    'erickmambergermail@yandex.ru', [f'{target_email}'], fail_silently=False,)
    except Exception as ex:
        text = f'Отправка сообщения пользователю на почту неудалась. Рекомендуется связаться с клиентом.\nОшибка: {ex}'

    send_mail(f'Новый клиент {time}', f'Время: {time}\nКонтакты: {target_email}, {target_phone}\n\n{text}',
                'erickmambergermail@yandex.ru', [f'mamberger.zhanna@yandex.ru'], fail_silently=False,)

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def test_mail():
    subject = 'Subject'
    html_message = render_to_string('main/index.html', {'context': 'values'})
    plain_message = strip_tags(html_message)
    from_email = 'erickmambergermail@yandex.ru'
    to = 'erickmambergermail@gmail.com'

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)