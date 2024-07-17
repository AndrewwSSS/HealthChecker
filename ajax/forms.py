from django.contrib.auth.forms import UserChangeForm
from django import forms

from main.models import (User,
                         Approach,
                         PowerTraining,
                         Meal,
                         DishCount,
                         Exercise,
                         PowerTrainingExercise)


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


class ApproachForm(forms.ModelForm):
    weight = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ApproachForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Approach
        fields = "__all__"

    def clean(self):
        cleaned_data = super(ApproachForm, self).clean()
        training = cleaned_data.get("training")
        try:
            PowerTraining.objects.get(user=self.request.user, exercises=training)
        except PowerTraining.DoesNotExist:
            raise forms.ValidationError("You have not training with this id")
        return cleaned_data


class DishCountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DishCountForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DishCount
        fields = ["weight", "meal", "dish"]

    def clean(self):
        cleaned_data = super(DishCountForm, self).clean()
        meal = cleaned_data.get("meal")

        if meal.user != self.user:
            raise forms.ValidationError("Invalid meal")

        return cleaned_data


class PowerExercisesForm(forms.ModelForm):
    class Meta:
        model = PowerTrainingExercise
        fields = "__all__"

