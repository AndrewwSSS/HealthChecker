from django.urls import path, include
from rest_framework import routers

from ajax.training_views import (
    CreatePowerExerciseView,
    DeleteCycling,
    DeletePowerTraining,
    DeletePowerTrainingExerciseView,
    DeleteSwimming,
    DeleteWalking,
    ApproachViewSet,
)
from ajax.user_statistics_views import (
    GetAvgCaloriesPerDayInfo,
    GetAvgCarbohydratesPerDayView,
    GetAvgFatsPerDayView,
    GetAvgProteinPerDayView,
    GetPFCratio,
    GetTotalKMbyCycling,
    GetTotalKMbyJogging,
    GetTotalKMbySwimming,
    GetTotalKMbyWalking,
    GetTrainingsTypeRatioView,
)
from ajax.user_views import UpdatePasswordView, UserUpdateView
from ajax.views import (
    DeleteDishView,
    DeleteExerciseView,
    DeleteMealView,
    DishCountViewSet,
)

router = routers.DefaultRouter()
router.register(r"dish-counts", DishCountViewSet, basename="dish-counts")
router.register(r"approaches", ApproachViewSet, basename="approaches")

urlpatterns = [
    path('', include(router.urls)),
    path(
        "user/me",
        UserUpdateView.as_view(),
        name="update-user"
    ),
    path(
        "user/me/update_password",
        UpdatePasswordView.as_view(),
        name="change-password"
    ),
    path(
        "power-training-exercises/",
        CreatePowerExerciseView.as_view(),
        name="create-power-training-exercise",
    ),
    path(
        "power-training-exercises/<int:pk>",
        DeletePowerTrainingExerciseView.as_view(),
        name="delete-power-training-exercise",
    ),
    path(
        "cycling/<int:pk>",
        DeleteCycling.as_view(),
        name="delete-cycling",
    ),
    path(
        "walking/<int:pk>",
        DeleteWalking.as_view(),
        name="delete-walking",
    ),
    path(
        "swimming/<int:pk>",
        DeleteSwimming.as_view(),
        name="delete-swimming",
    ),
    path(
        "jogging/<int:pk>",
        DeleteSwimming.as_view(),
        name="delete-jogging",
    ),
    path(
        "power-trainings/<int:pk>",
        DeletePowerTraining.as_view(),
        name="delete-power-training"
    ),
    path(
        "exercises/<int:pk>/",
        DeleteExerciseView.as_view(),
        name="delete-exercise"
    ),
    path(
        "dishes/<int:pk>/",
        DeleteDishView.as_view(),
        name="delete-dish"
    ),
    path(
        "meals/<int:pk>/",
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
