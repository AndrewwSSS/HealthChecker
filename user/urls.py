from django.urls import path

from user.statistics_views import (
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
from user.api_views import UpdatePasswordView, UserUpdateView


urlpatterns = [
    path(
        "me",
        UserUpdateView.as_view(),
        name="update-user"
    ),
    path(
        "me/update_password",
        UpdatePasswordView.as_view(),
        name="change-password"
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

app_name = "user"
