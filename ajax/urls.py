from django.urls import path

from ajax.views import (UpdatePasswordView,
                        UpdateUser,
                        AddPowerExerciseView,
                        CreateApproachView,
                        DeleteTrainingView,
                        DeleteApproach,
                        DeletePowerExerciseView,
                        AddDishCountView,
                        DeleteDishCountView,
                        UpdateApproachView,
                        UpdateDishCountView,
                        DeleteExerciseView,
                        DeleteDishView)

urlpatterns = [
    path("user_update", UpdateUser.as_view(), name="user-update"),
    path("change_password", UpdatePasswordView.as_view(), name="change-password"),
    path("add_power_training_exercise", AddPowerExerciseView.as_view(), name="add_power-training-exercise"),
    path("delete_power_exercise", DeletePowerExerciseView.as_view(), name="delete-power-exercise"),
    path("delete_approach", DeleteApproach.as_view(), name="delete-approach"),
    path("add_approach", CreateApproachView.as_view(), name="add-approach"),
    path("trainings/delete_training", DeleteTrainingView.as_view(), name="delete-training"),
    path("add_dish_to_meal", AddDishCountView.as_view(), name="add-dish-to-meal"),
    path("delete_dish_count", DeleteDishCountView.as_view(), name="delete-dish-count"),
    path("update_approach", UpdateApproachView.as_view(), name="update-approach"),
    path("update_dish_count", UpdateDishCountView.as_view(), name="update-dish-count"),
    path("delete_exercise", DeleteExerciseView.as_view(), name="delete-exercise"),
    path("delete_dish", DeleteDishView.as_view(), name="delete-dish"),
]

app_name = 'ajax'
