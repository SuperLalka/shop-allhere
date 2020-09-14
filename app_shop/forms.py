from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.models import User
from operator import itemgetter

from shop_allhere.utils import transliterate


class SearchForm(forms.Form):
    search_key = forms.CharField(label='Search', max_length=30)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.field_class = 'col-12 p-0'


class SubscriptionForm(forms.Form):
    user_mail = forms.EmailField(label='Email', max_length=40)

    def __init__(self, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.field_class = 'd-none d-xl-block col-12 pr-1'


class OrderForm(forms.Form):
    customer = forms.CharField(label="Заказчик", max_length=50,
                               help_text="необязательное для заполнения поле", required=False)
    customer_phone = forms.CharField(label="Номер телефона", max_length=20,
                                     help_text="необязательное для заполнения поле", required=False,
                                     widget=forms.TextInput(attrs={'placeholder': '+7'}))
    address = forms.CharField(label="Укажите адрес для доставки (формат 'Город, улица, дом')",
                              max_length=100,
                              help_text="Текст не более 100 символов",
                              widget=forms.Textarea(attrs={'rows': 1}))


class AuthorizationForm(forms.Form):
    username = forms.CharField(label="Представьтесь", max_length=60)
    password = forms.CharField(label="Введите пароль", max_length=30, widget=forms.PasswordInput)

    def clean_user_name(self):
        data = self.cleaned_data['user_name']
        if not User.objects.filter(username=data).exists():
            raise forms.ValidationError('Пользователь не существует')
        return data


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label="Представьтесь", max_length=60)
    email = forms.EmailField(label="Ввведите ваш E-mail", max_length=30)
    password = forms.CharField(label="Введите пароль", max_length=30, widget=forms.PasswordInput)
    password_check = forms.CharField(label="Пожалуйста, повторите ваш пароль", max_length=30,
                                     widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('Пользователь с данным именем уже существует')
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Введённый email уже используется')
        return data

    def clean_password_check(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_check']:
            raise forms.ValidationError('Введённые пароли не совпадают')
        return self.cleaned_data['password']


class PriceForm(forms.Form):
    price = forms.FloatField(label="", min_value=1, required=False)

    def __init__(self, *args, min_value, **kwargs):
        super(PriceForm, self).__init__(*args, **kwargs)
        self.fields['price'] = forms.FloatField(
            label="",
            min_value=min_value,
            required=False
        )


class VariableFiltersForm(forms.Form):
    pass

    def __init__(self, *args, filters=None, **kwargs):
        super(VariableFiltersForm, self).__init__(*args, **kwargs)
        if filters:
            ordered_filters = sorted(filters, key=itemgetter('filter__priority'), reverse=True)
            for item in ordered_filters:
                if item['filter__type'] == "TXT":
                    self.fields[item['filter__name']] = forms.CharField(
                        label=item['filter__name'],
                        max_length=50,
                        required=False
                    )
                elif item['filter__type'] == "INT":
                    self.fields[item['filter__name']] = forms.FloatField(
                        label=item['filter__name'],
                        min_value=min(item['filter__values']),
                        max_value=max(item['filter__values']),
                        required=False,
                    )
                elif item['filter__type'] == "CSM":
                    choices = ((c, c) for c in set(item['filter__values']))
                    self.fields[item['filter__name']] = forms.MultipleChoiceField(
                        label=item['filter__name'],
                        choices=choices,
                        required=False,
                        widget=forms.CheckboxSelectMultiple,
                    )

                self.fields[item['filter__name']].type = item['filter__type']
                self.fields[item['filter__name']].slug = transliterate(item['filter__name'])

            self.helper = FormHelper()
            self.helper.form_show_labels = False
            self.helper.field_class = 'text-left'
