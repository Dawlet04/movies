from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Movie, Genres, Countries, Comment


class CustomUserRegistrationForm(UserCreationForm):
    phone_num = forms.CharField(
        max_length=13, 
        required=True, 
        help_text='+998XXXXXXXXX', 
        widget=forms.TextInput(attrs={'placeholder': '+998901234567'})
    )
    photo = forms.ImageField(required=False)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_num', 'photo', 'password1', 'password2']
    
    def clean_phone_num(self):
        pn = self.cleaned_data.get('phone_num')
        if not pn.startswith('+998'):
            raise forms.ValidationError('Номер должен начинаться с +998')
        if len(pn) != 13:
            raise forms.ValidationError('Номер должен содержать 13 символов')
        return pn


class MovieSearchForm(forms.Form):
    query = forms.CharField(
        max_length=250, 
        required=False, 
        label='Поиск', 
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите название фильма...', 
            'class': 'search-input'
        })
    )


class MovieFilterForm(forms.Form):
    AGE_RATINGS = [
        ('', 'Все'), 
        ('0+', '0+'), 
        ('6+', '6+'), 
        ('12+', '12+'), 
        ('16+', '16+'), 
        ('18+', '18+')
    ]
    
    SORT_OPTIONS = [
        ('', 'По умолчанию'), 
        ('title', 'По названию (А-Я)'), 
        ('-title', 'По названию (Я-А)'), 
        ('year', 'По году (старые)'), 
        ('-year', 'По году (новые)')
    ]
    
    genre = forms.ModelChoiceField(
        queryset=Genres.objects.all(), 
        required=False, 
        empty_label='Все жанры', 
        label='Жанр'
    )
    
    country = forms.ModelChoiceField(
        queryset=Countries.objects.all(), 
        required=False, 
        empty_label='Все страны', 
        label='Страна'
    )
    
    age = forms.ChoiceField(
        required=False, 
        label='Возраст', 
        choices=AGE_RATINGS
    )
    
    sort_by = forms.ChoiceField(
        required=False, 
        label='Сортировка', 
        choices=SORT_OPTIONS
    )


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_num', 'photo', 'card_number']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_num': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'username': '',
            'email': '',
            'phone_num': '',
            'photo': '',
            'card_number': '',
        }
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
            'phone_num': 'Телефон',
            'photo': 'Фото профиля',
            'card_number': 'Номер карты',
        }
    
    def clean_phone_num(self):
        phone = self.cleaned_data.get('phone_num')
        if phone:
            if not phone.startswith('+998'):
                raise forms.ValidationError('Номер должен начинаться с +998')
            if len(phone) != 13:
                raise forms.ValidationError('Номер должен содержать 13 символов')
        return phone


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'comment-input',
                'placeholder': 'Напишите ваш комментарий...',
                'rows': 4
            })
        }
        labels = {
            'text': ''
        }