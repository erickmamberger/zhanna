from django.core.mail import send_mail


def mailing(time, target_email, target_phone):
    text = 'Письмо с оповещением успешно отправленно на указанный клиентом email.'
    try:
        send_mail('Запись в адкатский кабинет', f'Здравствуйте!\nВы записаны на консультацию в {time}',
                    'erickmambergermail@yandex.ru', [f'{target_email}'], fail_silently=False,)
    except Exception as ex:
        text = f'Отправка сообщения пользователю на почту неудалась. Рекомендуется связаться с клиентом.\nОшибка: {ex}'

    send_mail(f'Новый клиент {time}', f'Время: {time}\nКонтакты: {target_email}, {target_phone}\n\n{text}',
                'erickmambergermail@yandex.ru', [f'mamberger.zhanna@yandex.ru'], fail_silently=False,)
