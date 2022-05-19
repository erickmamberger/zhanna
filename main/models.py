from django.db import models


class Tickets(models.Model):

    time = models.DateTimeField(verbose_name='Время')
    email_text = models.TextField(verbose_name='Текст письма')# blank true -  значит что поле необязательно к заполнению
    price = models.IntegerField(verbose_name='Стоимость')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    is_published = models.BooleanField(default=True, verbose_name="Свободно")
    phone = models.CharField(default='+7', max_length=12, verbose_name='Номер тел.')
    email = models.EmailField(default='x@x.ru', verbose_name='Email')
    str_date = models.CharField(max_length=50, db_index=True, blank=True)

    def save(self, *args, **kwargs):
        self.str_date = self.time.strftime('%m-%d %H:%M')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.str_date

    class Meta:
        verbose_name = 'Окно для записи'
        verbose_name_plural = 'Окна для записи'
        ordering = ['time']