from django import forms
from products.models.review import Review


class ReviewForm(forms.Form):
    class Meta:
        model = Review
        fields = ["user", "comment"],
