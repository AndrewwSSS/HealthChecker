from django.urls import path

from ajax.training_views import CreateApproachView
from ajax.training_views import CreatePowerExerciseView
from ajax.training_views import DeleteApproach
from ajax.training_views import DeletePowerExerciseView
from ajax.training_views import DeleteTrainingView
from ajax.user_statistics_views import GetAvgCaloriesPerDayInfo
from ajax.user_statistics_views import GetAvgCarbohydratesPerDayView
from ajax.user_statistics_views import GetAvgFatsPerDayView
from ajax.user_statistics_views import GetAvgProteinPerDayView
from ajax.user_statistics_views import GetPFCratio
from ajax.user_statistics_views import GetTotalKMbyCycling
from ajax.user_statistics_views import GetTotalKMbyJogging
from ajax.user_statistics_views import GetTotalKMbySwimming
from ajax.user_statistics_views import GetTotalKMbyWalking
from ajax.user_statistics_views import GetTrainingsTypeRatioView
from ajax.user_views import UpdatePasswordView
from ajax.user_views import UpdateUser
from ajax.views import (
    CreateDishCountView,
    DeleteDishCountView,
    UpdateApproachView,
    UpdateDishCountView,
    DeleteExerciseView,
    DeleteDishView,
    DeleteMealView,
)

urlpatterns = [
    path(
        "user_update",
        UpdateUser.as_view(),
        name="update-user"
    ),
    path(
        "change_password",
        UpdatePasswordView.as_view(),
        name="change-password"
    ),
    path(
        "add_power_training_exercise",
        CreatePowerExerciseView.as_view(),
        name="create-power-training-exercise",
    ),
    path(
        "delete_power_exercise",
        DeletePowerExerciseView.as_view(),
        name="delete-power-exercise",
    ),
    path(
        "delete_approach",
        DeleteApproach.as_view(),
        name="delete-approach"),
    path(
        "add_approach",
        CreateApproachView.as_view(),
        name="create-approach"),
    path(
        "trainings/delete_training",
        DeleteTrainingView.as_view(),
        name="delete-training",
    ),
    path(
        "add_dish_to_meal",
        CreateDishCountView.as_view(),
        name="create-dish-count"),
    path(
        "delete_dish_count",
        DeleteDishCountView.as_view(),
        name="delete-dish-count"
    ),
    path(
        "update_approach",
        UpdateApproachView.as_view(),
        name="update-approach"
    ),
    path(
        "update_dish_count",
        UpdateDishCountView.as_view(),
        name="update-dish-count"
    ),
    path(
        "delete_exercise",
        DeleteExerciseView.as_view(),
        name="delete-exercise"
    ),
    path(
        "delete_dish",
        DeleteDishView.as_view(),
        name="delete-dish"
    ),
    path(
        "delete_meal",
        DeleteMealView.as_view(),
        name="delete-meal"
    ),
    path(
        "get_training_type_ratio/",
        GetTrainingsTypeRatioView.as_view(),
        name="get-training-type-ratio",
    ),
    path(
        "get_avg_calories_info/",
        GetAvgCaloriesPerDayInfo.as_view(),
        name="get-calories-info",
    ),
    path(
        "get_avg_protein_info/",
        GetAvgProteinPerDayView.as_view(),
        name="get-avg-protein-info",
    ),
    path(
        "get_avg_carbohydrates_info/",
        GetAvgCarbohydratesPerDayView.as_view(),
        name="get-avg-carbohydrates-info",
    ),
    path(
        "get_avg_fats_info/",
        GetAvgFatsPerDayView.as_view(),
        name="get-avg-fats-info"
    ),
    path(
        "get_total_km_by_cycling/",
        GetTotalKMbyCycling.as_view(),
        name="get-total-km-by-cycling",
    ),
    path(
        "get_total_km_by_jogging/",
        GetTotalKMbyJogging.as_view(),
        name="get-total-km-by-jogging",
    ),
    path(
        "get_total_km_by_walking/",
        GetTotalKMbyWalking.as_view(),
        name="get-total-km-by-walking",
    ),
    path(
        "get_total_km_by_swimming/",
        GetTotalKMbySwimming.as_view(),
        name="get-total-km-by-swimming",
    ),
    path(
        "get_pfc_ratio/",
        GetPFCratio.as_view(),
        name="get-pfc-ratio"
    ),
]

app_name = "ajax"
