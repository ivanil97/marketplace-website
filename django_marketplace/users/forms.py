from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.password_validation import password_changed
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["email", "first_name", ]


class ProfileDataForm(forms.Form):
    profile_picture = forms.ImageField(required=False)
    first_name = forms.CharField(
        max_length=50,
        error_messages={
            'required': 'Поле имя не может быть пустым',
            'max_length': 'Длина имени не может превышать 50 символов',
        }
    )
    last_name = forms.CharField(
        required=False,
        max_length=50,
        error_messages={
            'max_length': 'Длина фамилии не может превышать 50 символов',
        }
    )
    email = forms.EmailField(
        error_messages={
            'required': 'Поле e-mail не может быть пустым',
            'invalid': 'Введите корректный e-mail',
        },
    )
    phone_number = forms.CharField(
        required=False,
        min_length=10,
        max_length=12,
        widget=forms.TextInput(attrs={
            'placeholder': '+7 (___) ___ - __ - __',
        }),
        error_messages={
            'max_length': 'Введите корректный номер телефона',
            'min_length': 'Введите корректный номер телефона',
        }
    )

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Тут можно изменить пароль',
        }),
    )

    password_reply = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль повторно',
        }),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_reply = cleaned_data.get('password_reply')

        if password and not password_reply:
            self.add_error('password_reply', 'Для обновления пароля введите пароль повторно')
        if password_reply and not password:
            self.add_error('password', 'Для обновления пароля заполните поле "Пароль"')
        if password and password_reply and password != password_reply:
            self.add_error('password_reply', 'Пароли не совпадают. Пожалуйста, попробуйте снова')

        return cleaned_data

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')

        if profile_picture:
            max_size = 2 * 1024 * 1024

            if profile_picture.size > max_size:
                raise ValidationError('Размер фото профиля не должен превышать 2 Мб')

        return profile_picture

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if len(phone_number) == 12:
            phone_number = phone_number[2:]
        elif len(phone_number) == 11:
            phone_number = phone_number[1:]

        return phone_number
