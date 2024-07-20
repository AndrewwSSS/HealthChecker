from datetime import datetime

from django.contrib.auth.forms import (UserCreationForm,
                                       AuthenticationForm)
from django.forms import ModelForm
from django import forms
from pytz import timezone

from main.models import (User,
                         PowerTraining,
                         Exercise,
                         Cycling,
                         Dish,
                         Jogging,
                         Swimming,
                         Walking,
                         Meal)


class BaseTrainingForm(ModelForm):
    class Meta:
        fields = [
            "start",
            "end",
            "description",
        ]

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start', None)
        end = cleaned_data.get('end', None)

        if not start:
            return cleaned_data

        # if start >= datetime.now():
        #     raise forms.ValidationError('Start date must be less or equal than now')
        #
        # if end and start > end:
        #     raise forms.ValidationError('Start must be less than end date')

        return cleaned_data


class DistanceAverageSpeedTrainingForm(BaseTrainingForm):
    class Meta:
        fields = BaseTrainingForm.Meta.fields + ["average_speed", "distance"]


def clean_base_training(cleaned_data) -> dict:
    start = cleaned_data.get('start', None)
    end = cleaned_data.get('end', None)

    if not start or not end:
        return cleaned_data

    if start < datetime.now():
        raise forms.ValidationError('Start date must be less than now')

    if start > end:
        raise forms.ValidationError('Start must be less than end date')

    return cleaned_data


def clean_distance_average_speed_trainings(cleaned_data) -> dict:
    cleaned_data = clean_base_training(cleaned_data)

    distance = cleaned_data.get('distance', None)
    average_speed = cleaned_data.get('average_speed', None)

    if distance and distance <= 0:
        raise forms.ValidationError("Distance must be greater than zero")
    if average_speed and average_speed <= 0:
        raise forms.ValidationError("Average speed must be greater than zero")

    return cleaned_data


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields


class PowerTrainingForm(BaseTrainingForm):
    description = forms.CharField(required=False)

    class Meta:
        model = PowerTraining
        fields = BaseTrainingForm.Meta.fields


class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ["name", "description"]


class CyclingForm(DistanceAverageSpeedTrainingForm):
    description = forms.CharField(required=False)

    class Meta:
        model = Cycling
        fields = DistanceAverageSpeedTrainingForm.Meta.fields + ["climb"]

    def clean(self):
        cleaned_data = super(DistanceAverageSpeedTrainingForm, self).clean()
        climb = cleaned_data.get("climb", None)
        if not climb:
            raise forms.ValidationError("Climb is required field")
        if climb < 0:
            raise forms.ValidationError("Climb must be greater than zero")
        return cleaned_data


class DishForm(ModelForm):
    class Meta:
        model = Dish
        fields = [
            "name",
            "carbohydrates",
            "fats",
            "protein",
            "calories"
        ]

    def clean(self):
        cleaned_data = super(DishForm, self).clean()
        protein = cleaned_data.get("protein", 0)
        carbohydrates = cleaned_data.get("carbohydrates", 0)
        fats = cleaned_data.get("fats", 0)

        if sum([protein, carbohydrates, fats]) >= 100:
            raise forms.ValidationError("Sum of protein, carbohydrates and fats must be less than 100")
        return cleaned_data


class JoggingForm(DistanceAverageSpeedTrainingForm):
    class Meta:
        model = Jogging
        fields = DistanceAverageSpeedTrainingForm.Meta.fields


class SwimmingForm(DistanceAverageSpeedTrainingForm):
    class Meta:
        model = Swimming
        fields = DistanceAverageSpeedTrainingForm.Meta.fields


class WalkingForm(DistanceAverageSpeedTrainingForm):
    class Meta:
        model = Walking
        fields = DistanceAverageSpeedTrainingForm.Meta.fields


class MealForm(ModelForm):
    class Meta:
        model = Meal
        fields = ["date"]


class DateSearchForm(forms.Form):
    choices = (
        ("DESC", "descending"),
        ("ASC", "ascending"),
    )
    date = forms.DateField(
        required=False,
    )
    sort = forms.ChoiceField(choices=choices, required=True)


class NameSearchForm(forms.Form):
    choices = (
        ("DESC", "descending"),
        ("ASC", "ascending"),
    )
    name = forms.CharField(
        required=False,
        max_length=128,
    )
    sort = forms.ChoiceField(choices=choices, required=True)


class UserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)
