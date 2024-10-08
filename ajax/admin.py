from django.contrib import admin

from main.models import (
    Cycling,
    Dish,
    DishCount,
    Exercise,
    Jogging,
    Meal,
    PowerTraining,
    Swimming,
    User,
    Walking,
)

admin.site.register(User)
admin.site.register(PowerTraining)
admin.site.register(Cycling)
admin.site.register(Jogging)
admin.site.register(Walking)
admin.site.register(Swimming)
admin.site.register(Dish)
admin.site.register(Meal)
admin.site.register(Exercise)
admin.site.register(DishCount)
