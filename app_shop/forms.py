from crispy_forms.helper import FormHelper
from django import forms


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
    customer = forms.CharField(
        label="Заказчик", max_length=50, help_text="необязательное для заполнения поле", required=False)
    customer_phone = forms.CharField(
        label="Номер телефона", max_length=20, help_text="необязательное для заполнения поле", required=False,
        widget=forms.TextInput(attrs={'placeholder': '+7'}))
    address = forms.CharField(
        label="Укажите адрес для доставки (формат 'Город, улица, дом')",
        max_length=100,
        help_text="Текст не более 100 символов",
        widget=forms.Textarea(attrs={'rows': 1}))


class AuthorizationForm(forms.Form):
    user_name = forms.CharField(label="Представьтесь", max_length=60)
    user_password = forms.CharField(label="Введите пароль", max_length=30)


class RegistrationForm(forms.Form):
    user_name = forms.CharField(label="Представьтесь", max_length=60)
    user_email = forms.EmailField(label="Ввведите ваш E-mail", max_length=30)
    user_password = forms.CharField(label="Введите пароль", max_length=30)
    user_password_check = forms.CharField(label="Пожалуйста, повторите ваш пароль", max_length=30)

    def clean_user_password_check(self):
        if self.cleaned_data['user_password'] != self.cleaned_data['user_password_check']:
            raise forms.ValidationError('Введённые пароли не совпадают')
        return self


class PriceForm(forms.Form):
    price = forms.IntegerField(label="", min_value=1)
