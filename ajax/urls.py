from django.urls import include, path
from rest_framework import routers

from ajax.training_views import (
    ApproachViewSet,
    CreatePowerExerciseView,
    DeleteCycling,
    DeletePowerTraining,
    DeletePowerTrainingExerciseView,
    DeleteSwimming,
    DeleteWalking,
    DeleteJogging,
)

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
        "cycling/<int:pk>/",
        DeleteCycling.as_view(),
        name="delete-cycling",
    ),
    path(
        "walking/<int:pk>/",
        DeleteWalking.as_view(),
        name="delete-walking",
    ),
    path(
        "swimming/<int:pk>/",
        DeleteSwimming.as_view(),
        name="delete-swimming",
    ),
    path(
        "jogging/<int:pk>/",
        DeleteJogging.as_view(),
        name="delete-jogging",
    ),
    path(
        "power-trainings/<int:pk>/",
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
]

app_name = "ajax"
