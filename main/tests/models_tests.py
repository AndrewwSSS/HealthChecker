from datetime import timedelta

from django.utils import timezone

from django.test import TestCase

from ajax.tests.view_tests import UserRequiredMixin
from main.models import (User,
                         PowerTraining,
                         Dish,
                         Meal,
                         DishCount,
                         Exercise)


class BaseTestCaseWithUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user1',
            password='<PASSW-4ORD>'
        )


class UserTests(TestCase):
    def test_body_mass_index(self):
        user_1 = User.objects.create_user(username='user1',
                                          password='<PASSW-4ORD>',
                                          weight=102,
                                          height=187)
        user_2 = User.objects.create_user(username='user2',
                                          password='<PASS43WO->',
                                          weight=102,)
        user_3 = User.objects.create_user(username='user3',
                                          password='<PASS43WO->',
                                          height=187,)
        self.assertEqual(user_1.body_mass_index, 29.2)
        self.assertEqual(user_2.body_mass_index, None)
        self.assertEqual(user_3.body_mass_index, None)


class TrainingTests(BaseTestCaseWithUser):
    def test_training_str(self):
        now = timezone.now()
        yesterday = now - timedelta(days=1)
        another_date = now - timedelta(days=2)

        training_1 = PowerTraining.objects.create(
            start=now,
            user=self.user
        )
        training_2 = PowerTraining.objects.create(
            start=yesterday,
            user=self.user
        )
        training_3 = PowerTraining.objects.create(
            start=another_date,
            user=self.user
        )

        self.assertEqual(str(training_1),
                         f"Today, {training_1.start.strftime("%H:%M")}")

        self.assertEqual(str(training_2),
                         f"Yesterday, {training_2.start.strftime("%H:%M")}")

        self.assertEqual(str(training_3),
                         training_3.start.strftime("%d/%m/%Y %H:%M"))


class DishTests(BaseTestCaseWithUser):
    def test_dish_str(self):
        dish = Dish.objects.create(
            name="Rice",
            calories=120,
            protein=5,
            carbohydrates=20,
            fats=0.9,
            user=self.user
        )
        self.assertEqual(str(dish), "Rice")


class MealTests(BaseTestCaseWithUser):
    def setUp(self):
        super().setUp()

        now = timezone.now()
        yesterday = now - timedelta(days=1)
        another_date = now - timedelta(days=2)
        self.meal_1 = Meal.objects.create(
            date=now,
            user=self.user,
        )
        self.meal_2 = Meal.objects.create(
            date=yesterday,
            user=self.user,
        )
        self.meal_3 = Meal.objects.create(
            date=another_date,
            user=self.user,
        )
        self.meal_4 = Meal.objects.create(
            date=another_date,
            user=self.user,
        )

        self.dish_1 = Dish.objects.create(
            name="Rice",
            calories=120,
            protein=5,
            carbohydrates=20,
            fats=0.9,
            user=self.user
        )
        self.dish_2 = Dish.objects.create(
            name="cucumber",
            calories=30,
            protein=50,
            carbohydrates=10,
            fats=10,
            user=self.user
        )
        self.dish_3 = Dish.objects.create(
            name="fry potato",
            calories=300,
            protein=20,
            carbohydrates=20,
            fats=20,
            user=self.user
        )

        self.dish_count_1 = DishCount.objects.create(
            dish=self.dish_1,
            meal=self.meal_1,
            weight=100
        )
        self.dish_count_2 = DishCount.objects.create(
            dish=self.dish_2,
            meal=self.meal_1,
            weight=100
        )

        self.dish_count_3 = DishCount.objects.create(
            dish=self.dish_3,
            meal=self.meal_2,
            weight=200
        )

        self.dish_count_4 = DishCount.objects.create(
            dish=self.dish_2,
            meal=self.meal_3,
            weight=300
        )

    def test_meal_str(self):
        self.assertEqual(str(self.meal_1),
                         f"Today, {self.meal_1.date.strftime("%H:%M")}")

        self.assertEqual(str(self.meal_2),
                         f"Yesterday, {self.meal_2.date.strftime("%H:%M")}")

        self.assertEqual(str(self.meal_3),
                         self.meal_3.date.strftime("%d/%m/%Y %H:%M"))

    def test_total_calories(self):
        self.assertEqual(self.meal_1.get_total_calories(),
                         150)
        self.assertEqual(self.meal_2.get_total_calories(),
                         600)
        self.assertEqual(self.meal_3.get_total_calories(),
                         90)
        self.assertEqual(self.meal_4.get_total_calories(),
                         0)

    def test_total_fats(self):
        self.assertEqual(self.meal_1.get_total_fats(),
                         10.9)
        self.assertEqual(self.meal_2.get_total_fats(),
                         40)
        self.assertEqual(self.meal_3.get_total_fats(),
                         30)
        self.assertEqual(self.meal_4.get_total_fats(),
                         0)

    def test_total_protein(self):
        self.assertEqual(self.meal_1.get_total_protein(),
                         55)
        self.assertEqual(self.meal_2.get_total_protein(),
                         40)
        self.assertEqual(self.meal_3.get_total_protein(),
                         150)
        self.assertEqual(self.meal_4.get_total_protein(),
                         0)

    def test_total_carbohydrates(self):
        self.assertEqual(self.meal_1.get_total_carbohydrates(),
                         30)
        self.assertEqual(self.meal_2.get_total_carbohydrates(),
                         40)
        self.assertEqual(self.meal_3.get_total_carbohydrates(),
                         30)
        self.assertEqual(self.meal_4.get_total_carbohydrates(),
                         0)


class DishCountTests(BaseTestCaseWithUser):
    def setUp(self):
        super().setUp()
        now = timezone.now()
        self.meal_1 = Meal.objects.create(
            date=now,
            user=self.user,
        )
        self.meal_2 = Meal.objects.create(
            date=now,
            user=self.user,
        )
        self.meal_3 = Meal.objects.create(
            date=now,
            user=self.user,
        )
        self.dish_1 = Dish.objects.create(
            name="fry potato",
            calories=120,
            protein=5,
            carbohydrates=20,
            fats=0.9,
            user=self.user
        )

        self.dish_count_1 = DishCount.objects.create(
            dish=self.dish_1,
            meal=self.meal_1,
            weight=153
        )
        self.dish_count_2 = DishCount.objects.create(
            dish=self.dish_1,
            meal=self.meal_2,
            weight=399
        )

        self.dish_count_3 = DishCount.objects.create(
            dish=self.dish_1,
            meal=self.meal_3,
            weight=255
        )

    def test_calories(self):
        self.assertEqual(self.dish_count_1.calories, 183.6)
        self.assertEqual(self.dish_count_2.calories, 478.8)
        self.assertEqual(self.dish_count_3.calories, 306)

    def test_fats(self):
        self.assertEqual(self.dish_count_1.fats, 1.4)
        self.assertEqual(self.dish_count_2.fats, 3.6)
        self.assertEqual(self.dish_count_3.fats, 2.3)

    def test_carbohydrates(self):
        self.assertEqual(self.dish_count_1.carbohydrates, 30.6)
        self.assertEqual(self.dish_count_2.carbohydrates, 79.8)
        self.assertEqual(self.dish_count_3.carbohydrates, 51)

    def test_protein(self):
        self.assertEqual(self.dish_count_1.protein, 7.7)
        self.assertEqual(self.dish_count_2.protein, 20)
        self.assertEqual(self.dish_count_3.protein, 12.8)


class ExerciseTests(UserRequiredMixin, TestCase):
    def test_exercise_str(self):
        self.exercise = Exercise.objects.create(
            user=self.user,
            name="Test"
        )
        self.assertEqual(str(self.exercise), "Test")
