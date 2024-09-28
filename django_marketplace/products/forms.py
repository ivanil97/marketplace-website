from django import forms
from products.models.review import Review
from products.models.product import Product


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["comment"]


class SearchForm(forms.Form):
    query = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'range-line',
                'name': 'price',
                'type': 'text',
                'data-type': 'double',
                'data-min': '7',
                'data-max': '350',
                'data-from': '7',
                'data-to': '27'
            },
        ),
        label='',
    )


class SearchForm1(forms.Form):
    query1 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-input form-input_full',
                'name': 'title',
                'type': 'text',
                'id': 'title',
                'placeholder': 'Название',
            },
        ),
        label='',
        required=False,
    )
