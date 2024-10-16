from django import forms

from users.forms import ProfileDataForm
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['products']


class OrderProceedForm(ProfileDataForm):

    DELIVERY_OPTIONS = [
        ('ordinary', 'Обычная доставка'),
        ('express', 'Экспресс доставка'),
    ]
    PAYMENT_OPTIONS = [
        ('online', 'Онлайн картой'),
        ('someone', 'Онлайн со случайного чужого счета'),
    ]

    delivery_option = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=DELIVERY_OPTIONS
    )
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=PAYMENT_OPTIONS
    )
    city = forms.CharField(
        max_length=50,
        error_messages={
            'required': 'Поле город не может быть пустым',
            'max_length': 'Длина поля не может превышать 50 символов',
        }
    )
    address = forms.CharField(
        max_length=100,
        error_messages={
            'required': 'Поле адрес не может быть пустым',
            'max_length': 'Длина поля не может превышать 100 символов',
        }
    )

class PaymentDataForm(forms.Form):

    card_number = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        card_number = cleaned_data.get('card_number')
        card_number = ''.join(card_number.split())
        cleaned_data['card_number'] = card_number

        return cleaned_data