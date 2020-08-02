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


class ApplicationForOrderingForm(forms.Form):
    the_contact_person = forms.CharField(label="Контактное лицо", max_length=100)
    tin_of_the_organization = forms.CharField(label="ИНН Организации")
    email = forms.EmailField(label="E-mail", max_length=40)
    contact_phone_number = forms.CharField(label="Номер телефона для связи", initial="+7")
    order_list = forms.CharField(label="Состав заказа (список и количество позиций)", max_length=1000, help_text="Сумма заказа должна быть от 50 000 рублей", widget=forms.Textarea(attrs={'rows': 4}))
