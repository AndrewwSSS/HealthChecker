from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm
from django.utils import timezone

from main.models import (
    Cycling,
    Dish,
    Exercise,
    Jogging,
    Meal,
    PowerTraining,
    Swimming,
    User,
    Walking,
)


class BaseTrainingForm(ModelForm):
    class Meta:
        fields = [
            "start",
            "end",
            "description",
        ]

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start", None)
        end = cleaned_data.get("end", None)
        if not start:
            return cleaned_data
        if timezone.is_naive(start):
            start = timezone.make_aware(start)
        now = timezone.now()
        if start > now:
            raise forms.ValidationError("Start date must be less "
                                        "or equal to now")
        if end and start >= end:
            raise forms.ValidationError("Start must be less "
                                        "than end date")
        return cleaned_data


class DistanceAverageSpeedTrainingForm(BaseTrainingForm):
    class Meta:
        fields = BaseTrainingForm.Meta.fields + ["average_speed", "distance"]


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields


class PowerTrainingForm(BaseTrainingForm):
    class Meta:
        model = PowerTraining
        fields = BaseTrainingForm.Meta.fields


class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ["name", "description"]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name", None)

        if (not self.instance.id
                and Exercise.objects.filter(name=name).exists()):
            raise forms.ValidationError("Exercise with this "
                                        "name already exists")

        return cleaned_data


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
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DishForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Dish
        fields = ["name", "carbohydrates", "fats", "protein", "calories"]

    def clean(self):
        cleaned_data = super(DishForm, self).clean()

        protein = cleaned_data.get("protein", 0)
        carbohydrates = cleaned_data.get("carbohydrates", 0)
        fats = cleaned_data.get("fats", 0)

        if sum([protein, carbohydrates, fats]) >= 100:
            raise forms.ValidationError(
                "Sum of protein, carbohydrates "
                "and fats must be less than 100"
            )

        name = cleaned_data.get("name")

        if self.user.dishes.filter(name__iexact=name).exists():
            raise forms.ValidationError("Dish with this name already exists")

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
    start_date = forms.DateField(
        required=False,
    )
    end_date = forms.DateField(
        required=False,
    )
    sort = forms.ChoiceField(choices=choices, required=False)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date", None)
        end_date = cleaned_data.get("end_date", None)

        if start_date and start_date > timezone.now().date():
            raise forms.ValidationError("Start date must be less "
                                        "or equal than now")
        if end_date and end_date > timezone.now().date():
            raise forms.ValidationError("End date must be less "
                                        "or equal than now")
        if end_date and start_date and start_date > end_date:
            raise forms.ValidationError("End date must be grater than "
                                        "start date")
        return cleaned_data


class NameSearchForm(forms.Form):
    choices = (
        ("DESC", "descending"),
        ("ASC", "ascending"),
    )
    name = forms.CharField(
        required=False,
        max_length=128,
    )
    sort = forms.ChoiceField(choices=choices, required=False)


class UserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)
