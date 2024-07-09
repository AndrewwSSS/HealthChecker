from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from main.models import User, PowerTraining, Exercise


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields


class PowerTrainingForm(ModelForm):
    class Meta:
        model = PowerTraining
        fields = ["start", "end", "description", "user"]


class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ["name", "description"]