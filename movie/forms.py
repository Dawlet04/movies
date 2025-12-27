from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Movie, Genres, Countries


class CustomUserRegistrationForm(UserCreationForm):
    phone_num = forms.CharField(max_length=13, required=True, help_text='+998XXXXXXXXX', 
                                 widget=forms.TextInput(attrs={'placeholder': '+998901234567'}))
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
    query = forms.CharField(max_length=250, required=False, label='Поиск', 
                           widget=forms.TextInput(attrs={'placeholder': 'Введите название фильма...', 
                                                         'class': 'search-input'}))



class AdvancedMovieSearchForm(forms.Form):
    year_choices = [('', 'Все годы')]
    for y in range(2024, 1949, -1):
        year_choices.append((str(y), str(y)))
    
    AGE_RATINGS = [('', 'Все'), ('0+', '0+'), ('6+', '6+'), ('12+', '12+'), 
                   ('16+', '16+'), ('18+', '18+')]
    
    SORT_OPTIONS = [
        ('', 'По умолчанию'), 
        ('title', 'По названию (А-Я)'), 
        ('-title', 'По названию (Я-А)'), 
        ('year', 'По году (старые)'), 
        ('-year', 'По году (новые)'),
        ('rating', 'По рейтингу (низкий)'),
        ('-rating', 'По рейтингу (высокий)'),
    ]
    
    
    title = forms.CharField(max_length=250, required=False, label='Название фильма',
                           widget=forms.TextInput(attrs={'placeholder': 'Название...', 
                                                         'class': 'form-control'}))
    
    director = forms.CharField(max_length=200, required=False, label='Режиссер',
                              widget=forms.TextInput(attrs={'placeholder': 'Имя режиссера...', 
                                                            'class': 'form-control'}))
    
    actor = forms.CharField(max_length=200, required=False, label='Актер',
                           widget=forms.TextInput(attrs={'placeholder': 'Имя актера...', 
                                                         'class': 'form-control'}))
    
    genre = forms.ModelMultipleChoiceField(
        queryset=Genres.objects.all(), 
        required=False, 
        label='Жанры',
        widget=forms.CheckboxSelectMultiple
    )
    
    country = forms.ModelChoiceField(
        queryset=Countries.objects.all(), 
        required=False, 
        empty_label='Все страны', 
        label='Страна',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    year_from = forms.ChoiceField(
        required=False, 
        label='Год от', 
        choices=year_choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    year_to = forms.ChoiceField(
        required=False, 
        label='Год до', 
        choices=year_choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    age = forms.ChoiceField(
        required=False, 
        label='Возрастной рейтинг', 
        choices=AGE_RATINGS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    
    min_rating = forms.DecimalField(
        required=False, 
        label='Минимальный рейтинг',
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={'placeholder': '0.0', 'class': 'form-control', 'step': '0.1'})
    )
    
    sort_by = forms.ChoiceField(
        required=False, 
        label='Сортировка', 
        choices=SORT_OPTIONS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )



class MovieFilterForm(forms.Form):
    AGE_RATINGS = [('', 'Все'), ('0+', '0+'), ('6+', '6+'), ('12+', '12+'), 
                   ('16+', '16+'), ('18+', '18+')]
    
    SORT_OPTIONS = [('', 'По умолчанию'), ('title', 'По названию (А-Я)'), 
                    ('-title', 'По названию (Я-А)'), ('year', 'По году (старые)'), 
                    ('-year', 'По году (новые)')]
    
    genre = forms.ModelChoiceField(
        queryset=Genres.objects.all(), 
        required=False, 
        empty_label='Все жанры', 
        label='Жанр',
        widget=forms.Select(attrs={'class': 'filter-select'})  
    )
    
    country = forms.ModelChoiceField(
        queryset=Countries.objects.all(), 
        required=False, 
        empty_label='Все страны', 
        label='Страна',
        widget=forms.Select(attrs={'class': 'filter-select'}) 
    )
    
    age = forms.ChoiceField(
        required=False, 
        label='Возраст', 
        choices=AGE_RATINGS,
        widget=forms.Select(attrs={'class': 'filter-select'})  
    )
    
    sort_by = forms.ChoiceField(
        required=False, 
        label='Сортировка', 
        choices=SORT_OPTIONS,
        widget=forms.Select(attrs={'class': 'filter-select'})  
    )

    class ProfileEditForm(forms.ModelForm):
        class Meta:
            model = CustomUser
        fields = ['username', 'email', 'phone_num', 'photo', 'card_number']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'phone_num': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998901234567'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'card_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '9860xxxxyyyyzzzz'
            }),
        }
    
    def clean_phone_num(self):
        phone = self.cleaned_data.get('phone_num')
        if phone and not phone.startswith('+998'):
            raise forms.ValidationError('Номер должен начинаться с +998')
        if phone and len(phone) != 13:
            raise forms.ValidationError('Номер должен содержать 13 символов')
        return phone