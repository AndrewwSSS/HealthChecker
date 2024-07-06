from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from main.models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields


