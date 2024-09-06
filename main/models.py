from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import (
    CheckConstraint,
    ForeignKey,
    Q,
    UniqueConstraint,
)
from django.utils import timezone


def convert_datetime_to_string(value) -> str:
    now = timezone.now()
    if value.date() == (now - timedelta(days=1)).date():
        return f"Yesterday, {value.strftime('%H:%M')}"
    elif value.date() == now.date():
        return f"Today, {value.strftime('%H:%M')}"
    else:
        return value.strftime("%d/%m/%Y %H:%M")


class User(AbstractUser):
    SEX_CHOICES = (
        (
            "F",
            "Female",
        ),
        (
            "M",
            "Male",
        ),
        (
            "U",
            "Unsure",
        ),
    )
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, null=True)
    birth_date = models.DateField(
        null=True,
    )
    weight = models.FloatField(
        null=True, validators=[MinValueValidator(20), MaxValueValidator(400)]
    )
    height = models.IntegerField(
        null=True, validators=[MinValueValidator(140), MaxValueValidator(250)]
    )

    @property
    def body_mass_index(self) -> float | None:
        if not self.weight or not self.height:
            return None
        return round((self.weight / (self.height**2)) * 10000, 1)


class Training(models.Model):
    user = ForeignKey(get_user_model(), on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True
        ordering = ["-start"]
        constraints = [
            CheckConstraint(
                check=Q(start__lt=models.F("end")),
                name="%(app_label)s_%(class)s_end_date_grater_than_start_date",
            ),
        ]

    def __str__(self):
        return convert_datetime_to_string(self.start)


class Approach(models.Model):
    weight = models.FloatField(default=0, validators=[MinValueValidator(0)])
    repeats = models.IntegerField(validators=[MinValueValidator(1)])
    training = models.ForeignKey(
        "PowerTrainingExercise",
        on_delete=models.CASCADE,
        related_name="approaches"
    )


class Exercise(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="exercises"
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class PowerTrainingExercise(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    power_training = models.ForeignKey(
        "PowerTraining", related_name="exercises", on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["exercise", "power_training"],
                name="unique_power_training_exercise",
            ),
        ]


class PowerTraining(Training):
    pass


class DistanceAverageSpeedMixin(models.Model):
    average_speed = models.FloatField(validators=[MinValueValidator(1)])
    distance = models.FloatField(validators=[MinValueValidator(1)])

    class Meta:
        abstract = True


class Cycling(Training, DistanceAverageSpeedMixin):
    climb = models.FloatField(validators=[MinValueValidator(1)])


class Swimming(Training, DistanceAverageSpeedMixin):
    pass


class Walking(Training, DistanceAverageSpeedMixin):
    pass


class Jogging(Training, DistanceAverageSpeedMixin):
    pass


class Dish(models.Model):
    name = models.CharField(max_length=255)
    calories = models.FloatField(validators=[MinValueValidator(0.1)])
    protein = models.FloatField(validators=[MinValueValidator(0.1)])
    carbohydrates = models.FloatField(validators=[MinValueValidator(0.1)])
    fats = models.FloatField(validators=[MinValueValidator(0.1)])
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="dishes"
    )

    class Meta:
        ordering = ["name"]
        constraints = [
            UniqueConstraint(
                fields=["user", "name"],
                name="unique_dish_name_for_user"
            )
        ]

    def __str__(self):
        return self.name


class DishCount(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    meal = models.ForeignKey(
        "Meal",
        on_delete=models.CASCADE,
        related_name="dishes"
    )
    weight = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            UniqueConstraint(fields=["dish", "meal"],
                             name="unique_dish_for_meal"),
        ]

    @property
    def calories(self) -> float:
        return round(self.dish.calories * (self.weight / 100), 1)

    @property
    def fats(self) -> float:
        return round(self.dish.fats * (self.weight / 100), 1)

    @property
    def carbohydrates(self) -> float:
        return round(self.dish.carbohydrates * (self.weight / 100), 1)

    @property
    def protein(self) -> float:
        return round(self.dish.protein * (self.weight / 100), 1)


class Meal(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="meals"
    )

    class Meta:
        ordering = ["-date"]

    @property
    def calories(self):
        return sum(dish.calories for dish in self.dishes.all())

    @property
    def fats(self):
        return sum(dish.fats for dish in self.dishes.all())

    @property
    def protein(self):
        return sum(dish.protein for dish in self.dishes.all())

    @property
    def carbohydrates(self):
        return sum(dish.carbohydrates for dish in self.dishes.all())

    def __str__(self):
        return convert_datetime_to_string(self.date)
