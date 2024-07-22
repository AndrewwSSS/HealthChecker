from datetime import datetime, date

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from main.models import User, Exercise, PowerTraining, PowerTrainingExercise, Approach, Swimming, Walking, Jogging, \
    Cycling, Meal, Dish, DishCount


class LoginRequiredPostMixin(object):
    def test_loging_required(self):
        client = Client()
        response = client.post(self.url)
        self.assertEqual(response.status_code, 302)


class LoginRequiredGetMixin(object):
    def test_loging_required(self):
        client = Client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 302)


class UserRequiredMixin(object):
    def setUp(self):
        self.user_password = "<PASSWO32RD>"
        self.user = User.objects.create_user(
            username='testuser',
            password=self.user_password,
        )
        self.another_user = User.objects.create_user(
            username='Aboba_user',
            password="<PASS432WORD>",
        )
        self.client.force_login(self.user)


class UpdatePasswordViewTests(LoginRequiredPostMixin, UserRequiredMixin, TestCase):
    url = reverse("api:change-password")

    def test_change_password(self):
        new_password = "lkmgsdlp43-ds"
        form_data = {
            "old_password": self.user_password,
            "new_password1": new_password,
            "new_password2": new_password,
        }
        response = self.client.post(self.url, form_data)
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.check_password(new_password))

    def test_change_password_fail(self):
        form_data = {
            "old_password": "Wrong password",
            "new_password1": "123542",
            "new_password2": "123242",
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 422)


class UpdateUserTests(LoginRequiredGetMixin, UserRequiredMixin, TestCase):
    url = reverse("api:update-user")

    def test_update_user(self):
        form_data = {
            "username": "testuser1590",
            "sex": "M",
            "email": "email_mail@gmail.com",
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": "02/01/1999",
        }
        response = self.client.post(self.url, form_data)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.username, "testuser1590")
        self.assertEqual(self.user.sex, "M"),
        self.assertEqual(self.user.email, "email_mail@gmail.com")
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.birth_date, date(1999, 2, 1))

    def test_update_user_fail(self):
        form_data = {
            "username": self.another_user.username,
        }
        response = self.client.post(self.url, form_data)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 422)
        self.assertNotEqual(self.user.username, self.another_user.username)


class CreatePowerExerciseViewTests(LoginRequiredPostMixin, UserRequiredMixin, TestCase):
    url = reverse("api:create-power-training-exercise")

    def setUp(self):
        super().setUp()
        self.exercise = Exercise.objects.create(
            name="Test Exercise",
            user=self.user,
        )
        self.power_training = PowerTraining.objects.create(
            start=timezone.now(),
            user=self.user
        )

    def test_create_power_exercise(self):
        form_data = {
            "exercise": self.exercise.id,
            "training": self.power_training.id,
        }

        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.power_training.exercises.filter(id=response.json()["id"]).exists())

    def test_create_power_exercise_duplicate(self):
        new_exercise = PowerTrainingExercise.objects.create(
            exercise=self.exercise,
            power_training=self.power_training,
        )
        form_data = {
            "exercise": self.exercise.id,
            "training": self.power_training.id,
        }
        response = self.client.post(self.url, form_data)
        self.assertNotEqual(response.status_code, 200)


class CreateApproachViewTests(LoginRequiredPostMixin, UserRequiredMixin, TestCase):
    url = reverse("api:create-approach")

    def setUp(self):
        super().setUp()
        self.exercise = Exercise.objects.create(
            name="Test Exercise",
            user=self.user,
        )
        self.power_training = PowerTraining.objects.create(
            start=timezone.now(),
            user=self.user
        )
        self.power_exercise = PowerTrainingExercise.objects.create(
            exercise=self.exercise,
            power_training=self.power_training,
        )
        self.power_training.exercises.add(self.power_exercise)

    def test_create_approach(self):
        form_data = {
            "weight": 100,
            "repeats": 20,
            "training": self.power_exercise.id
        }
        response = self.client.post(self.url, form_data)
        self.power_exercise.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        approach_queryset = self.power_exercise.approaches.filter(id=response.json()["id"])
        self.assertTrue(approach_queryset.exists())
        approach = approach_queryset.first()
        self.assertEqual(approach.weight, 100)
        self.assertEqual(approach.repeats, 20)

    def test_create_approach_another_user(self):
        self.client.force_login(self.another_user)
        form_data = {
            "weight": 100,
            "repeats": 20,
            "training": self.power_exercise.id
        }
        response = self.client.post(self.url, form_data)
        self.assertNotEqual(response.status_code, 200)
        approach_queryset = self.power_exercise.approaches.filter(id=self.power_exercise.id)
        self.assertFalse(approach_queryset.exists())


class DeleteApproachViewTests(LoginRequiredPostMixin, UserRequiredMixin, TestCase):
    url = reverse("api:delete-approach")

    def setUp(self):
        super().setUp()
        self.exercise = Exercise.objects.create(
            name="Test Exercise",
            user=self.user,
        )
        self.power_training = PowerTraining.objects.create(
            start=timezone.now(),
            user=self.user
        )
        self.power_exercise = PowerTrainingExercise.objects.create(
            exercise=self.exercise,
            power_training=self.power_training,
        )
        self.approach = Approach.objects.create(
            weight=100,
            repeats=20,
            training=self.power_exercise,
        )

    def test_delete_approach(self):
        form_data = {
            "approach": self.approach.id,
            "exercise": self.power_exercise.id,
        }
        response = self.client.post(self.url, form_data)
        self.power_exercise.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.power_exercise.approaches.filter(id=self.approach.id).exists())

    def test_delete_approach_another_user(self):
        self.client.force_login(self.another_user)
        form_data = {
            "approach": self.approach.id,
            "exercise": self.power_exercise.id,
        }

        response = self.client.post(self.url, form_data)
        self.power_exercise.refresh_from_db()
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(self.power_exercise.approaches.filter(id=self.approach.id).exists())


class DeletePowerTrainingExerciseViewTests(LoginRequiredPostMixin, UserRequiredMixin, TestCase):
    url = reverse("api:delete-power-exercise")

    def setUp(self):
        super().setUp()
        self.exercise = Exercise.objects.create(
            name="Test Exercise",
            user=self.user,
        )
        self.power_training = PowerTraining.objects.create(
            start=timezone.now(),
            user=self.user
        )
        self.power_exercise = PowerTrainingExercise.objects.create(
            exercise=self.exercise,
            power_training=self.power_training,
        )

    def test_delete_power_exercise(self):
        form_data = {
            "exercise": self.power_exercise.id,
        }

        response = self.client.post(self.url, form_data)
        self.power_training.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.power_training.exercises.filter(id=self.power_exercise.id).exists())

    def test_delete_power_exercise_another_user(self):
        self.client.force_login(self.another_user)
        form_data = {
            "exercise": self.power_exercise.id,
        }

        response = self.client.post(self.url, form_data)
        self.power_training.refresh_from_db()
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(self.power_training.exercises.filter(id=self.power_exercise.id).exists())


class DeleteTrainingViewTests(LoginRequiredPostMixin, UserRequiredMixin, TestCase):
    url = reverse("api:delete-training")

    def setUp(self):
        super().setUp()
        self.swimming = Swimming.objects.create(
            start=timezone.now(),
            distance=10,
            average_speed=10,
            user=self.user
        )
        self.jogging = Jogging.objects.create(
            start=timezone.now(),
            distance=10,
            average_speed=10,
            user=self.user
        )
        self.walking = Walking.objects.create(
            start=timezone.now(),
            distance=10,
            average_speed=10,
            user=self.user
        )
        self.cycling = Cycling.objects.create(
            start=timezone.now(),
            distance=10,
            climb=10,
            average_speed=10,
            user=self.user
        )
        self.power_training = PowerTraining.objects.create(
            start=timezone.now(),
            user=self.user
        )

    def test_delete_swimming(self):
        form_data = {
            "id": self.swimming.id,
            "type": "SW"
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Swimming.objects.filter(id=self.swimming.id).exists())

    def test_delete_jogging(self):
        form_data = {
            "id": self.jogging.id,
            "type": "JG"
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Jogging.objects.filter(id=self.jogging.id).exists())

    def test_delete_walking(self):
        form_data = {
            "id": self.walking.id,
            "type": "WK"
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Walking.objects.filter(id=self.walking.id).exists())

    def test_delete_cycling(self):
        form_data = {
            "id": self.cycling.id,
            "type": "CY"
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Cycling.objects.filter(id=self.cycling.id).exists())

    def test_delete_power_training(self):
        form_data = {
            "id": self.power_training.id,
            "type": "PW"
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(PowerTraining.objects.filter(id=self.power_training.id).exists())

    def test_delete_swimming_another_user(self):
        self.client.force_login(self.another_user)
        form_data = {
            "id": self.swimming.id,
            "type": "SW"
        }
        response = self.client.post(self.url, form_data)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(Swimming.objects.filter(id=self.swimming.id).exists())

    def test_delete_jogging_another_user(self):
        self.client.force_login(self.another_user)
        form_data = {
            "id": self.jogging.id,
            "type": "JG"
        }
        response = self.client.post(self.url, form_data)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(Jogging.objects.filter(id=self.jogging.id).exists())

    def test_delete_walking_another_user(self):
        self.client.force_login(self.another_user)
        form_data = {
            "id": self.walking.id,
            "type": "WK"
        }
        response = self.client.post(self.url, form_data)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(Walking.objects.filter(id=self.walking.id).exists())

    def test_delete_cycling_another_user(self):
        self.client.force_login(self.another_user)
        form_data = {
            "id": self.cycling.id,
            "type": "CY"
        }
        response = self.client.post(self.url, form_data)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(Cycling.objects.filter(id=self.cycling.id).exists())

    def test_delete_power_training_another_user(self):
        self.client.force_login(self.another_user)
        form_data = {
            "id": self.power_training.id,
            "type": "PW"
        }
        response = self.client.post(self.url, form_data)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(PowerTraining.objects.filter(id=self.power_training.id).exists())


class CreateDishCountViewTests(LoginRequiredPostMixin, UserRequiredMixin, TestCase):
    url = reverse("api:create-dish-count")

    def setUp(self):
        super().setUp()
        self.meal = Meal.objects.create(
            date=timezone.now(),
            user=self.user,
        )
        self.dish = Dish.objects.create(
            name="Test dish",
            calories=100,
            fats=20,
            protein=10,
            carbohydrates=10,
            user=self.user
        )

    def test_create_dish_count(self):
        form_data = {
            "dish": self.dish.id,
            "meal": self.meal.id,
            "weight": 400
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        dish_count_query_set = self.meal.dishes.filter(id=self.dish.id)
        self.assertTrue(dish_count_query_set.exists())
        dish_count = dish_count_query_set.first()

        self.assertEqual(dish_count.weight, 400)
        self.assertEqual(dish_count.dish, self.dish)

    def test_create_dish_count_another_user(self):
        self.client.force_login(self.another_user)
        form_data = {
            "dish": self.dish.id,
            "meal": self.meal.id,
            "weight": 400
        }
        response = self.client.post(self.url, form_data)
        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(self.meal.dishes.filter(id=self.dish.id).exists())


class UpdateDishCountViewTests(LoginRequiredPostMixin, UserRequiredMixin, TestCase):
    url = reverse("api:update-dish-count")

    def setUp(self):
        super().setUp()
        self.meal = Meal.objects.create(
            date=timezone.now(),
            user=self.user,
        )
        self.dish = Dish.objects.create(
            name="Test dish",
            calories=100,
            fats=20,
            protein=10,
            carbohydrates=10,
            user=self.user
        )
        self.dish_count_weight = 400
        self.dish_count = DishCount.objects.create(
            dish=self.dish,
            meal=self.meal,
            weight=self.dish_count_weight
        )

    def test_update_dish_count(self):
        form_data = {
            "dish_count": self.dish_count.id,
            "meal": self.meal.id,
            "weight": 999
        }

        response = self.client.post(self.url, form_data)
        self.dish_count.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.dish_count.weight, 999)
        self.assertEqual(self.dish_count.dish, self.dish)
        self.assertEqual(self.dish_count.meal, self.meal)

    def test_update_dish_count_another_user(self):
        self.client.force_login(self.another_user)
        form_data = {
            "dish_count": self.dish_count.id,
            "meal": self.meal.id,
            "weight": 999
        }
        response = self.client.post(self.url, form_data)
        self.dish_count.refresh_from_db()
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(self.dish_count.weight, self.dish_count_weight)
        self.assertEqual(self.dish_count.dish, self.dish)
        self.assertEqual(self.dish_count.meal, self.meal)


class DeleteDishCountViewTests(LoginRequiredPostMixin, UserRequiredMixin, TestCase):
    url = reverse("api:delete-dish-count")

    def setUp(self):
        super().setUp()
        self.meal = Meal.objects.create(
            date=timezone.now(),
            user=self.user,
        )
        self.dish = Dish.objects.create(
            name="Test dish",
            calories=100,
            fats=20,
            protein=10,
            carbohydrates=10,
            user=self.user
        )
        self.dish_count_weight = 400
        self.dish_count = DishCount.objects.create(
            dish=self.dish,
            meal=self.meal,
            weight=self.dish_count_weight
        )

    def test_delete_dish_count(self):
        form_data = {
            "dish_count": self.dish_count.id,
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.meal.dishes.filter(id=self.dish_count.id).exists())

    def test_delete_dish_count_another_user(self):
        self.client.force_login(self.another_user)
        form_data = {
            "dish_count": self.dish_count.id,
        }
        response = self.client.post(self.url, form_data)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(self.meal.dishes.filter(id=self.dish_count.id).exists())


class UpdateApproachViewTests(LoginRequiredPostMixin, UserRequiredMixin, TestCase):
    url = reverse("api:update-approach")

    def setUp(self):
        super().setUp()
        self.power_training = PowerTraining.objects.create(
            user=self.user,
            start=timezone.now(),
        )
        self.exercise = Exercise.objects.create(
            user=self.user,
            name="Test exercise",
        )
        self.power_training_exercise = PowerTrainingExercise.objects.create(
            exercise=self.exercise,
            power_training=self.power_training
        )
        self.approach_weight = 100
        self.approach_repeats = 22
        self.approach = Approach.objects.create(
            training=self.power_training_exercise,
            weight=100,
            repeats=self.approach_repeats
        )

    def test_update_approach(self):
        form_data = {
            "weight": 122,
            "id": self.approach.id,
            "training": self.approach.training.id,
            "repeats": 22
        }
        response = self.client.post(self.url, form_data)
        self.approach.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.approach.weight, 122)
        self.assertEqual(self.approach.repeats, 22)

    def test_update_approach_another_user(self):
        self.client.force_login(self.another_user)
        form_data = {
            "weight": 122,
            "id": self.approach.id,
            "repeats": 22
        }
        response = self.client.post(self.url, form_data)
        self.approach.refresh_from_db()
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(self.approach.weight, self.approach_weight)
        self.assertEqual(self.approach.repeats, self.approach_repeats)


class DeleteExerciseViewTests(LoginRequiredPostMixin, UserRequiredMixin, TestCase):
    url = reverse("api:delete-exercise")

    def setUp(self):
        super().setUp()
        self.exercise = Exercise.objects.create(
            user=self.user,
            name="Test exercise",
        )

    def test_delete_exercise(self):
        form_data = {
            "exercise_id": self.exercise.id
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Exercise.objects.filter(id=self.exercise.id).exists())

    def test_delete_exercise_another_user(self):
        self.client.force_login(self.another_user)
        form_data = {
            "exercise_id": self.exercise.id
        }
        response = self.client.post(self.url, form_data)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(Exercise.objects.filter(id=self.exercise.id).exists())


class DeleteDishViewTests(LoginRequiredPostMixin, UserRequiredMixin, TestCase):
    url = reverse("api:delete-dish")

    def setUp(self):
        super().setUp()
        self.dish = Dish.objects.create(
            name="Test dish",
            calories=100,
            fats=20,
            protein=10,
            carbohydrates=10,
            user=self.user
        )

    def test_delete_dish(self):
        form_data = {
            "id": self.dish.id
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Dish.objects.filter(id=self.dish.id).exists())

    def test_delete_dish_another_user(self):
        self.client.force_login(self.another_user)
        form_data = {
            "id": self.dish.id
        }
        response = self.client.post(self.url, form_data)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(Dish.objects.filter(id=self.dish.id).exists())


class DeleteMealViewTests(LoginRequiredPostMixin, UserRequiredMixin, TestCase):
    url = reverse("api:delete-meal")

    def setUp(self):
        super().setUp()
        self.meal = Meal.objects.create(
            date=timezone.now(),
            user=self.user,
        )

    def test_delete_meal(self):
        form_data = {
            "id": self.meal.id,
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Meal.objects.filter(id=self.meal.id).exists())

    def test_delete_meal_another_user(self):
        self.client.force_login(self.another_user)
        form_data = {
            "id": self.meal.id,
        }
        response = self.client.post(self.url, form_data)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(Meal.objects.filter(id=self.meal.id).exists())


class GetTrainingTypeRatio(LoginRequiredGetMixin, UserRequiredMixin, TestCase):
    url = reverse("api:get-training-type-ratio")

    def setUp(self):
        super().setUp()

        self.power_training = PowerTraining.objects.create(
            user=self.user,
            start=timezone.now() - timezone.timedelta(days=1),
        )
        self.cycling = Cycling.objects.create(
            user=self.user,
            start=timezone.now(),
            distance=50,
            climb=150,
            average_speed=15
        )
        self.walking = Walking.objects.create(
            user=self.user,
            start=timezone.now(),
            distance=50,
            average_speed=6
        )

    def test_get_training_type_ratio_month(self):
        period = "Today"
        response = self.client.get(self.url + "?period={0}".format(period))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.url + "?period={0}".format(period))
        data = response.json()
        valid_data = {
            "data": [
                {
                    "name": "Power trainings",
                    "value": 0,
                },
                {
                    "name": "Cycling",
                    "value": 1,
                },
                {
                    "name": "Jogging",
                    "value": 0,
                },
                {
                    "name": "Walking",
                    "value": 1,
                },
                {
                    "name": "Swimming",
                    "value": 0,
                },
            ]
        }
        self.assertEqual(data, valid_data)


