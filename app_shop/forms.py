from crispy_forms.helper import FormHelper
from django import forms


class SearchForm(forms.Form):
    search_key = forms.CharField(label='Search', max_length=30)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.field_class = 'col-12 p-0'
