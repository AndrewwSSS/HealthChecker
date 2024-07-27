from django.urls import path

from main.views import (
    HomePageView,
    CreateUserView,
    logout_view,
    UserProfileView,
    PowerTrainingsListView,
    ExercisesListView,
    ExerciseUpdateView,
    ExerciseCreateView,
    UpdatePowerTrainingView,
    CyclingTrainingListView,
    CreateCyclingTrainingView,
    CreatePowerTrainingView,
    DishListView,
    CreateDishView,
    UpdateDishView,
    UpdateCyclingTrainingView,
    SwimmingTrainingListView,
    WalkingTrainingListView,
    JoggingTrainingListView,
    CreateSwimmingView,
    CreateWalkingView,
    CreateJoggingView,
    UpdateSwimmingView,
    UpdateJoggingView,
    UpdateWalkingView,
    MealListView,
    CreateMealView,
    UpdateMealView,
    LoginUserView,
)

urlpatterns = [
    path(
        "",
        HomePageView.as_view(),
        name="home"
    ),
    path(
        "home/",
        HomePageView.as_view(),
        name="home"
    ),
    path(
        "power-trainings/",
        PowerTrainingsListView.as_view(),
        name="power-trainings-list",
    ),
    path(
        "power-trainings/create",
        CreatePowerTrainingView.as_view(),
        name="create-power-training",
    ),
    path(
        "account/registration",
        CreateUserView.as_view(),
        name="registration"
    ),
    path(
        "accounts/login",
        LoginUserView.as_view(),
        name="login"
    ),
    path(
        "accounts/logout",
        logout_view,
        name="logout"
    ),
    path(
        "accounts/user-profile",
        UserProfileView.as_view(),
        name="user-profile"
    ),
    path(
        "exercises/",
        ExercisesListView.as_view(),
        name="exercises-list"
    ),
    path(
        "exercise/<int:pk>",
        ExerciseUpdateView.as_view(),
        name="exercise-update"
    ),
    path(
        "exercises/create/",
        ExerciseCreateView.as_view(),
        name="create-exercise"
    ),
    path(
        "power-trainings/update/<int:pk>",
        UpdatePowerTrainingView.as_view(),
        name="update-power-training",
    ),
    path(
        "cycling-trainings/",
        CyclingTrainingListView.as_view(),
        name="cycling-training-list",
    ),
    path(
        "cycling-trainings/create",
        CreateCyclingTrainingView.as_view(),
        name="create-cycling-training",
    ),
    path(
        "cycling-trainings/update/<int:pk>",
        UpdateCyclingTrainingView.as_view(),
        name="update-cycling-training",
    ),
    path(
        "dishes/",
        DishListView.as_view(),
        name="dish-list"
    ),
    path(
        "dishes/create",
        CreateDishView.as_view(),
        name="create-dish"
    ),
    path(
        "dishes/update/<int:pk>",
        UpdateDishView.as_view(),
        name="update-dish"
    ),
    path(
        "swimming-trainings/",
        SwimmingTrainingListView.as_view(),
        name="swimming-training-list",
    ),
    path(
        "walking-trainings/",
        WalkingTrainingListView.as_view(),
        name="walking-training-list",
    ),
    path(
        "jogging-trainings/",
        JoggingTrainingListView.as_view(),
        name="jogging-training-list",
    ),
    path(
        "swimming-trainings/create",
        CreateSwimmingView.as_view(),
        name="create-swimming-training",
    ),
    path(
        "walking-trainings/create",
        CreateWalkingView.as_view(),
        name="create-walking-training",
    ),
    path(
        "jogging-traings/create",
        CreateJoggingView.as_view(),
        name="create-jogging-training",
    ),
    path(
        "swimming-trainings/update/<int:pk>",
        UpdateSwimmingView.as_view(),
        name="update-swimming-training",
    ),
    path(
        "jogging-traings/update/<int:pk>",
        UpdateJoggingView.as_view(),
        name="update-jogging-training",
    ),
    path(
        "walking-trainings/update/<int:pk>",
        UpdateWalkingView.as_view(),
        name="update-walking-training",
    ),
    path(
        "meals/",
        MealListView.as_view(),
        name="meal-list"
    ),
    path(
        "meals/create",
        CreateMealView.as_view(),
        name="create-meal"
    ),
    path(
        "meals/update/<int:pk>",
        UpdateMealView.as_view(),
        name="update-meal"
    ),
]

app_name = "main"
