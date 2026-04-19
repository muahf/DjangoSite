from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Pathogen, Researcher


class UmbrellaAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
            if isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs.setdefault('autocomplete', 'current-password')
        self.fields['username'].widget.attrs.setdefault('autocomplete', 'username')


class RegistrationForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Идентификатор оператора',
            'autocomplete': 'username',
        }),
    )
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••',
            'autocomplete': 'new-password',
        }),
    )
    password_confirm = forms.CharField(
        label='Повтор пароля',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
            'autocomplete': 'new-password',
        }),
    )

    def clean_username(self):
        name = self.cleaned_data['username'].strip()
        if User.objects.filter(username__iexact=name).exists():
            raise ValidationError('Этот логин уже занят.')
        return name

    def clean(self):
        data = super().clean()
        p1, p2 = data.get('password'), data.get('password_confirm')
        if p1 and p2 and p1 != p2:
            raise ValidationError('Пароли не совпадают.')
        return data

    def save(self):
        return User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
        )


class PathogenForm(forms.ModelForm):

    transmission = forms.MultipleChoiceField(
        choices=Pathogen.TRANSMISSION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Способ передачи"
    )

    class Meta:
        model = Pathogen
        fields = [
            'title',
            'description',
            'image',
            'author',
            'creator',
            'family',
            'origin',
            'discovered',
            'application',
            'transmission',
            'is_available'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название патогена'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание патогена...'
            }),
            'family': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Семейство'
            }),
            'origin': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Происхождение'
            }),
            'discovered': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата открытия'
            }),
            'application': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Применение'
            }),
        }

        labels = {
            'title': 'Название',
            'description': 'Описание',
            'image': 'Изображение',
            'author': 'Исследователь',
            'creator': 'Создатель',
            'family': 'Семейство',
            'origin': 'Происхождение',
            'discovered': 'Дата открытия',
            'application': 'Применение',
            'is_available': 'Безопасен?',
        }


# ✅ ВАЖНО: ОТДЕЛЬНО ОТ ВСЕХ КЛАССОВ
class ResearcherForm(forms.ModelForm):
    class Meta:
        model = Researcher
        fields = ['name', 'email']

        labels = {
            'name': 'Имя',
            'email': 'Электронная почта',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя исследователя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
        }