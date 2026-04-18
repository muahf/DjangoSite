from django import forms
from .models import Pathogen, Researcher


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