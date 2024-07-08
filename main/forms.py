from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from main.models import User, PowerTraining


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields


class TrainingCreateForm(ModelForm):
    class Meta:
        model = PowerTraining
        fields = ["start", "end", "description", "user"]

