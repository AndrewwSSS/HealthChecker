from django.urls import path

from ajax.views import (UpdatePasswordView,
                        UpdateUser,
                        AddPowerExerciseView,
                        AddApproachView,
                        DeleteTrainingView,
                        DeleteApproach,
                        DeleteExerciseView,
                        AddDishCountView,
                        DeleteDishCountView, UpdateApproachView)

urlpatterns = [
    path("user_update", UpdateUser.as_view(), name="user_update"),
    path("change_password", UpdatePasswordView.as_view(), name="change_password"),
    path("add_power_training_exercise", AddPowerExerciseView.as_view(), name="add_power_training_exercise"),
    path("delete_exercise", DeleteExerciseView.as_view(), name="delete_exercise"),
    path("delete_approach", DeleteApproach.as_view(), name="delete_approach"),
    path("add_approach", AddApproachView.as_view(), name="add_approach"),
    path("trainings/delete_training", DeleteTrainingView.as_view(), name="delete_training"),
    path("add_dish_to_meal", AddDishCountView.as_view(), name="add_dish_to_meal"),
    path("delete_dish_count", DeleteDishCountView.as_view(), name="delete_dish_count"),
    path("update_approach", UpdateApproachView.as_view(), name="update_approach"),
]

app_name = 'ajax'
