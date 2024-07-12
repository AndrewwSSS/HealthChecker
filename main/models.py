from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import (ForeignKey,
                              UniqueConstraint,
                              CheckConstraint,
                              Q)


class Training(models.Model):
    user = ForeignKey("User", on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True
        constraints = [
            CheckConstraint(check=Q(start__lt=models.F("end")),
                            name="end_date_grater_than_start_date"),
        ]


class Approach(models.Model):
    weight = models.FloatField(default=0,
                               validators=[MinValueValidator(0)])
    repeats = models.IntegerField(validators=[MinValueValidator(0)])
    training = models.ForeignKey("PowerTrainingExercise",
                                 on_delete=models.CASCADE,
                                 related_name="approaches")


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name


class PowerTrainingExercise(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
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
    average_speed = models.FloatField(validators=[MinValueValidator(0)])
    distance = models.FloatField(validators=[MinValueValidator(0)])

    class Meta:
        abstract = True


class Cycling(Training, DistanceAverageSpeedMixin):
    climb = models.FloatField(validators=[MinValueValidator(0)])


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
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="dishes")

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "name"], name="unique_dish_name_for_user")
        ]

    def __str__(self):
        return self.name


class DishCount(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    meal = models.ForeignKey("Meal", on_delete=models.CASCADE, related_name="dishes")
    weight = models.FloatField(validators=[MinValueValidator(1)])


class Meal(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey("User", on_delete=models.CASCADE)


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
    birth_date = models.DateField(null=True)
    weight = models.FloatField(null=True,
                               validators=[MinValueValidator(20), MaxValueValidator(400)])
    height = models.IntegerField(null=True,
                                 validators=[MinValueValidator(140), MaxValueValidator(250)])

    @property
    def body_mass_index(self):
        return
