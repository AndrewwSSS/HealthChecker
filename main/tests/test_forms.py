from django.test import TestCase
from django.utils import timezone

from main.forms import (
    CyclingForm,
    DishForm,
    ExerciseForm,
    JoggingForm,
    PowerTrainingForm,
)
from main.models import (
    Dish,
    Exercise,
    User,
)


class BaseTrainingFormTests(TestCase):
    def test_training_is_valid(self):
        form_data = {
            "start": timezone.now(),
            "end": timezone.now() + timezone.timedelta(hours=1),
        }
        form = PowerTrainingForm(form_data)
        self.assertTrue(form.is_valid())

    def test_training_start_grater_than_end(self):
        form_data = {
            "start": timezone.now(),
            "end": timezone.now() - timezone.timedelta(hours=1),
        }
        form = PowerTrainingForm(form_data)
        self.assertFalse(form.is_valid())

    def test_start_grater_than_now(self):
        form_data = {
            "start": timezone.now() + timezone.timedelta(hours=1),
        }
        form = PowerTrainingForm(form_data)
        self.assertFalse(form.is_valid())


class DistanceAverageSpeedTrainingFormTests(TestCase):
    def test_training_has_fields(self):
        form_data = {
            "start": timezone.now(),
            "average_speed": 15.0,
            "distance": 50.0,
            "description": "lorem ipsum",
            "end": None,
        }
        form = JoggingForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class ExerciseFormTests(TestCase):
    def test_form_has_fields(self):
        form_data = {
            "name": "<NAME>",
            "description": "lorem ipsum",
        }
        form = ExerciseForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_unique_name(self):
        self.user = User.objects.create_user(
            username="Aboba",
            password="<PA54SSWORD>",
        )
        Exercise.objects.create(
            name="<NAME>", description="lorem ipsum", user=self.user
        )
        form_data = {
            "name": "<NAME>",
            "description": "lorem ipsum",
        }
        form = ExerciseForm(data=form_data)
        self.assertFalse(form.is_valid())


class CyclingFormTests(TestCase):
    def test_form_has_fields(self):
        form_data = {
            "start": timezone.now(),
            "end": None,
            "description": "lorem ipsum",
            "distance": 50.0,
            "climb": 10.0,
            "average_speed": 15.0,
        }
        form = CyclingForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_invalid_climb(self):
        form_data = {
            "start": timezone.now() + timezone.timedelta(hours=1),
            "distance": 50.0,
            "climb": -10,
            "average_speed": 15.0,
        }
        form = CyclingForm(data=form_data)
        self.assertFalse(form.is_valid())


class DishFormTests(TestCase):
    def test_form_has_fields(self):
        form_data = {
            "name": "test",
            "carbohydrates": 10.0,
            "protein": 10.0,
            "fats": 10.0,
            "calories": 103,
        }
        form = DishForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_invalid_nutrients_sum(self):
        form_data = {
            "name": "test",
            "carbohydrates": 20,
            "protein": 70.0,
            "fats": 30.0,
            "calories": 103,
        }
        form = DishForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_unique_name(self):
        self.user = User.objects.create_user(
            username="Aboba",
            password="<PASSWORD>",
        )
        form_data = {
            "name": "test",
            "carbohydrates": 10.0,
            "protein": 10.0,
            "fats": 10.0,
            "calories": 103,
        }
        Dish.objects.create(**form_data, user=self.user)

        form = DishForm(data=form_data)
        self.assertFalse(form.is_valid())
