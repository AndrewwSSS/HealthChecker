from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import (ForeignKey,
                              UniqueConstraint,
                              CheckConstraint,
                              Q,
                              Sum)
from django.utils import timezone


class User(AbstractUser):
    SEX_CHOICES = (
        ('F', 'Female',),
        ('M', 'Male',),
        ('U', 'Unsure',),
    )
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        null=True
    )
    birth_date = models.DateField(null=True,)
    weight = models.FloatField(null=True,
                               validators=[MinValueValidator(20), MaxValueValidator(400)])
    height = models.IntegerField(null=True,
                                 validators=[MinValueValidator(140), MaxValueValidator(250)])

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
        ordering = ['-start']
        constraints = [
            CheckConstraint(check=Q(start__lt=models.F("end")),
                            name="%(app_label)s_%(class)s_end_date_grater_than_start_date"),
        ]

    def __str__(self):
        now = timezone.now()
        if self.start.date() == (now - timedelta(days=1)).date():
            return f"Yesterday, {self.start.strftime("%H:%M")}"
        elif self.start.date() == now.date():
            return f"Today, {self.start.strftime("%H:%M")}"
        else:
            return self.start.strftime("%d/%m/%Y %H:%M")


class Approach(models.Model):
    weight = models.FloatField(default=0,
                               validators=[MinValueValidator(0)])
    repeats = models.IntegerField(validators=[MinValueValidator(1)])
    training = models.ForeignKey("PowerTrainingExercise",
                                 on_delete=models.CASCADE,
                                 related_name="approaches")


class Exercise(models.Model):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name="exercises")
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-name']


class PowerTrainingExercise(models.Model):
    exercise = models.ForeignKey(Exercise,
                                 on_delete=models.CASCADE)
    power_training = models.ForeignKey("PowerTraining",
                                       related_name="exercises",
                                       on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["exercise", "power_training"],
                             name="unique_power_training_exercise"),
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
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name="dishes")

    class Meta:
        ordering = ["name"]
        constraints = [
            UniqueConstraint(fields=["user", "name"], name="unique_dish_name_for_user")
        ]

    def __str__(self):
        return self.name


class DishCount(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    meal = models.ForeignKey("Meal",
                             on_delete=models.CASCADE,
                             related_name="dishes")
    weight = models.FloatField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            UniqueConstraint(fields=["dish", "meal"], name="unique_dish_for_meal"),
        ]

    @property
    def calories(self) -> float:
        return self.dish.calories * (self.weight / 100)

    @property
    def fats(self) -> float:
        return self.dish.fats * (self.weight / 100)

    @property
    def carbohydrates(self) -> float:
        return self.dish.carbohydrates * (self.weight / 100)

    @property
    def protein(self) -> float:
        return self.dish.protein * (self.weight / 100)


class Meal(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name="meals")

    class Meta:
        ordering = ["-date"]

    def get_total_calories(self):
        return sum(dish.calories for dish in self.dishes.all())

    def get_total_fats(self):
        return sum(dish.fats for dish in self.dishes.all())

    def get_total_protein(self):
        return sum(dish.protein for dish in self.dishes.all())

    def get_total_carbohydrates(self):
        return sum(dish.carbohydrates for dish in self.dishes.all())


