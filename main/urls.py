from django.urls import path

from main.views import (HomePageView,
                        CreateUserView,
                        logout_view,
                        UserProfileView,
                        PowerTrainingsListView,
                        ExercisesListView,
                        ExerciseUpdateView,
                        ExerciseCreateView,
                        PowerTrainingUpdateView,
                        CyclingTrainingListView,
                        CreateCyclingTrainingView,
                        CreatePowerTrainingView,
                        DishListView,
                        CreateDishView,
                        UpdateDishView)
from django.contrib.auth.views import LoginView


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("home/", HomePageView.as_view(), name="home"),
    path("power-trainings/", PowerTrainingsListView.as_view(), name="power-trainings-list"),
    path("power-trainings/create", CreatePowerTrainingView.as_view(), name="create-power-training"),
    path("account/registration", CreateUserView.as_view(), name="registration"),
    path("accounts/login", LoginView.as_view(), name="login"),
    path("accounts/logout", logout_view, name="logout"),
    path("accounts/user-profile", UserProfileView.as_view(), name="user-profile"),
    path("exercises/", ExercisesListView.as_view(), name="exercises-list"),
    path("exercise/<int:pk>", ExerciseUpdateView.as_view(), name="exercise-update"),
    path("exercises/create/", ExerciseCreateView.as_view(), name="create-exercise"),
    path("power-trainings/update/<int:pk>", PowerTrainingUpdateView.as_view(), name="update-power-training"),
    path("cycling-trainings/", CyclingTrainingListView.as_view(), name="cycling-training-list"),
    path("cycling-trainings/create", CreateCyclingTrainingView.as_view(), name="create-cycling-training"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/create", CreateDishView.as_view(), name="create-dish"),
    path("dishes/update/<int:pk>", UpdateDishView.as_view(), name="update-dish"),

]

app_name = "main"
