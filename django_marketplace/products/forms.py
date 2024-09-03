from django import forms
from products.models.review import Review


class FeedBackForm(forms.Form):
    class Meta:
        model = Review
        fields = "comment",
