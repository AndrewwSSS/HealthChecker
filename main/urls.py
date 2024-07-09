from django.urls import path

from main.views import HomePageView, CreateUserView, logout_view, UserProfileView, CreateTrainingView, \
    PowerTrainingsListView, ExercisesListView, ExerciseUpdateView, ExerciseCreateView, PowerTrainingUpdateView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("home/", HomePageView.as_view(), name="home"),
    path("power-trainings/", PowerTrainingsListView.as_view(), name="power-trainings-list"),
    path("trainings/create", CreateTrainingView.as_view(), name="create-training"),
    path("account/registration", CreateUserView.as_view(), name="registration"),
    path("accounts/login", LoginView.as_view(), name="login"),
    path("accounts/logout", logout_view, name="logout"),
    path("accounts/user-profile", UserProfileView.as_view(), name="user-profile"),
    path("exercises/", ExercisesListView.as_view(), name="exercises-list"),
    path("exercise/<int:pk>", ExerciseUpdateView.as_view(), name="exercise-update"),
    path("exercises/create/", ExerciseCreateView.as_view(), name="create-exercise"),
    path("power-trainings/update/<int:pk>", PowerTrainingUpdateView.as_view(), name="update-power-training"),
]

app_name = "main"
