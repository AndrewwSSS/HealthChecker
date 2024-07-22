from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ajax.tests.view_tests import UserRequiredMixin
from main.forms import DateSearchForm
from main.models import (User,
                         PowerTraining,
                         Meal, Dish,
                         Exercise)


class DateSearchTrainingListViewTests(UserRequiredMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.power_training_1 = PowerTraining.objects.create(
            user=self.user,
            start=timezone.now(),
        )
        self.power_training_2 = PowerTraining.objects.create(
            user=self.user,
            start=timezone.now() - timezone.timedelta(days=1),
        )

    def test_search_power_training_by_date(self):
        url = reverse("main:power-trainings-list")
        date = timezone.now().date()
        response = self.client.get(url + f"?date={date}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(self.power_training_1))
        self.assertNotContains(response, str(self.power_training_2))


class DateSearchListViewMixin(UserRequiredMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.meal_1 = Meal.objects.create(
            user=self.user,
            date=timezone.now(),
        )
        self.meal_2 = Meal.objects.create(
            user=self.user,
            date=timezone.now() - timezone.timedelta(days=1),
        )

    def test_search_power_training_by_date(self):
        url = reverse("main:meal-list")
        today = timezone.now().date()
        response = self.client.get(url + f"?date={today}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(self.meal_1))
        self.assertNotContains(response, str(self.meal_2))


class NameSearchListViewTests(UserRequiredMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.dish_1 = Dish.objects.create(
            user=self.user,
            name='Rice',
            calories=100,
            fats=43,
            protein=20,
            carbohydrates=10
        )
        self.dish_2 = Dish.objects.create(
            user=self.user,
            name='Cucumber',
            calories=100,
            fats=43,
            protein=20,
            carbohydrates=10
        )

        self.exercise_1 = Exercise.objects.create(
            name="Pull ups",
            user=self.user,
        )
        self.exercise_2 = Exercise.objects.create(
            name="test exer",
            user=self.user,
        )

    def test_search_dishes_by_name(self):
        url = reverse("main:dish-list")
        response = self.client.get(url + f"?name=ri")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(self.dish_1))
        self.assertNotContains(response, str(self.dish_2))

    def test_search_exercises_by_name(self):
        url = reverse("main:exercises-list")
        response = self.client.get(url + f"?name=pull")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(self.exercise_1))
        self.assertNotContains(response, str(self.exercise_2))
