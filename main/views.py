from datetime import datetime

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic

from main.forms import UserCreateForm, PowerTrainingForm, ExerciseForm, CyclingTrainingForm, DishForm
from main.models import User, PowerTraining, Exercise, CyclingTraining, Dish


class HomePageView(LoginRequiredMixin, generic.TemplateView):
    template_name = "main/index.html"
    login_url = "accounts/login"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context


class UserProfileView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = "main/user-detail.html"

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        return self.request.user


class CreateUserView(generic.CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "registration/registration.html"
    success_url = "/"


class CreatePowerTrainingView(LoginRequiredMixin, generic.CreateView):
    template_name = "main/create-power-training.html"
    model = PowerTraining
    form_class = PowerTrainingForm
    success_url = "/power-trainings/"


class PowerTrainingsListView(LoginRequiredMixin, generic.ListView):
    model = PowerTraining
    template_name = "main/power-trainings-list.html"


class ExercisesListView(LoginRequiredMixin, generic.ListView):
    model = Exercise
    template_name = "main/exercises-list.html"

    paginate_by = 30


class ExerciseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Exercise
    template_name = "main/exercise-form.html"
    success_url = "/exercises/"
    form_class = ExerciseForm


class ExerciseCreateView(LoginRequiredMixin, generic.CreateView):
    model = Exercise
    template_name = "main/exercise-form.html"
    form_class = ExerciseForm
    success_url = "/exercises/"

    
class PowerTrainingUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = PowerTraining
    template_name = "main/update-power-training.html"
    form_class = PowerTrainingForm
    success_url = "/power-trainings/"

    def get_context_data(self, **kwargs):
        context = super(PowerTrainingUpdateView, self).get_context_data(**kwargs)
        return context


class CyclingTrainingListView(LoginRequiredMixin, generic.ListView):
    model = CyclingTraining
    template_name = "main/cycling-training-list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CyclingTrainingListView, self).get_context_data(**kwargs)
        return context


class CreateCyclingTrainingView(LoginRequiredMixin, generic.CreateView):
    model = CyclingTraining
    form_class = CyclingTrainingForm
    template_name = "main/create-cycling-training.html"
    success_url = "/cycling-trainings/"


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    template_name = "main/dish-list.html"


class CreateDishView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    template_name = "main/create-dish.html"
    success_url = "/dishes/"


class UpdateDishView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    template_name = "main/update-dish.html"
    success_url = "/dishes/"


class UpdateCyclingTrainingView(LoginRequiredMixin, generic.UpdateView):
    model = CyclingTraining
    form = CyclingTrainingForm
    template_name = "main/update-cycling-training.html"


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect("/accounts/login")






