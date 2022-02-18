import uuid
from datetime import datetime

from yoomoney import Quickpay, Client
from django.core.mail import send_mail
from main.models import Tickets


def get_pay_link():
    uniq = str(uuid.uuid4().int)
    uniq = uniq[:6]
    quickpay = Quickpay(
                receiver="4100116993572215",
                quickpay_form="shop",
                targets="Пожалуйста, сохраните номер вашего платежа перед оплатой:"
                        f"\n{uniq}",
                paymentType="SB",
                successURL='http://127.0.0.1:8000/tickets/',
                sum=3,
                label=uniq,
            )
    pay_link = quickpay.redirected_url
    print(pay_link)
    return pay_link


def check_payment(id):
    # требуется импорт с .env yoomoney token
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
