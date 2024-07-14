from django.contrib.auth.forms import UserChangeForm
from django import forms

from main.models import User


class UserUpdateForm(UserChangeForm):
    birth_date = forms.DateField(required=False,
                                 widget=forms.DateInput(attrs={'type': 'date'}))
    weight = forms.IntegerField(required=False,
                                widget=forms.NumberInput(attrs={'type': 'number'}))
    height = forms.IntegerField(required=False,)
    sex = forms.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "birth_date",
            "weight",
            "height",
            "sex"
        ]
