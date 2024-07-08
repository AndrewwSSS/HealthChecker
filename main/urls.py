from django.urls import path

from main.views import HomePageView, CreateUserView, logout_view, UserProfileView, CreateTrainingView,PowerTrainingsListView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("home/", HomePageView.as_view(), name="home"),
    path("trainings/", PowerTrainingsListView.as_view(), name="power-trainings-list"),
    path("trainings/create", CreateTrainingView.as_view(), name="create-training"),
    path("account/registration", CreateUserView.as_view(), name="registration"),
    path("accounts/login", LoginView.as_view(), name="login"),
    path("accounts/logout", logout_view, name="logout"),
    path("accounts/user-profile", UserProfileView.as_view(), name="user-profile"),
]

app_name = "main"
