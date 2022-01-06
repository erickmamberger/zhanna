from django import forms
from django.core.exceptions import ValidationError

from main.service import get_actual_tickets


class TicketsForm(forms.Form):# Создаем на основе модели форму

    time = forms.CharField(widget=forms.Select(choices=get_actual_tickets()))#choices=get_actual_tickets())
    phone = forms.CharField(disabled='+7')
    email = forms.EmailField()
    payment_id = forms.CharField(max_length=255)

    def clean_recipients(self):
        data = self.cleaned_data['recipients']
        print(data)
        # if "fred@example.com" not in data:
        #     raise forms.ValidationError("You have forgotten about Fred!")
        #
        # # Always return a value to use as the new cleaned data, even if
        # # this method didn't change it.
        # return data