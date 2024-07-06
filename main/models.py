from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ForeignKey


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name


class Training(models.Model):
    user = ForeignKey("User", on_delete=models.CASCADE)
    start = models.DateField(auto_now_add=False)
    end = models.DateField()

    class Meta:
        abstract = True


class Approach(models.Model):
    date = models.DateField(auto_now_add=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    weight = models.FloatField()


class PowerTraining(Training):
    approaches = models.ManyToManyField(Approach)


class CyclingTraining(Training):
    average_speed = models.FloatField()
    distance = models.FloatField()
    climb = models.FloatField()
    duration = models.TimeField()


class SwimmingTraining(Training):
    average_speed = models.FloatField()
    distance = models.FloatField()
    duration = models.TimeField()


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    calories = models.FloatField()
    protein = models.FloatField()
    carbohydrates = models.FloatField()
    fats = models.FloatField()

    def __str__(self):
        return self.name


class DishCount(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    weight = models.FloatField()


class Meal(models.Model):
    date = models.DateField(auto_now_add=True)
    dishes = models.ManyToManyField(Dish)
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
    weight = models.FloatField(null=True)
    height = models.IntegerField(null=True)

    @property
    def body_mass_index(self):
        return
