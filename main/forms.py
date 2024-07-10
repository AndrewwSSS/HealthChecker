from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from main.models import User, PowerTraining, Exercise, CyclingTraining, Dish


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


class CyclingTrainingForm(ModelForm):
    class Meta:
        model = CyclingTraining
        fields = "__all__"

    def clean(self):
        # To keep the main validation and error messages
        super(CyclingTrainingForm, self).clean()


class DishForm(ModelForm):
    class Meta:
        model = Dish
        fields = "__all__"
