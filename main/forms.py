from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from main.models import (User,
                         PowerTraining,
                         Exercise,
                         Cycling,
                         Dish,
                         Jogging,
                         Swimming,
                         Walking,
                         Meal)


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


class CyclingForm(ModelForm):
    class Meta:
        model = Cycling
        fields = "__all__"


class DishForm(ModelForm):
    class Meta:
        model = Dish
        fields = "__all__"


class JoggingForm(ModelForm):
    class Meta:
        model = Jogging
        fields = "__all__"


class SwimmingForm(ModelForm):
    class Meta:
        model = Swimming
        fields = "__all__"


class WalkingForm(ModelForm):
    class Meta:
        model = Walking
        fields = "__all__"


class MealForm(ModelForm):
    class Meta:
        model = Meal
        fields = "__all__"
