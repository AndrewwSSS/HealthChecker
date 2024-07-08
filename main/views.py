from datetime import datetime

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from main.forms import UserCreateForm, TrainingCreateForm, ExerciseForm
from main.models import User, PowerTraining, Exercise


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


class CreateTrainingView(LoginRequiredMixin, generic.TemplateView):
    template_name = "main/create-training.html"

    def get_context_data(self, **kwargs):
        context = super(CreateTrainingView, self).get_context_data(**kwargs)
        context["default_start_date"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return context

    def get(self, request, *args, **kwargs):
        return render(request, "main/create-training.html", context=self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        form = TrainingCreateForm(request.POST)
        context = self.get_context_data(**kwargs)
        if form.is_valid():
            form.save()
            # TODO redirection to update view
        else:
            context["errors"] = form.errors
            context = context + request.POST
        return render(request, "main/create-training.html", context=context)


class PowerTrainingsListView(LoginRequiredMixin, generic.TemplateView):
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


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect("/accounts/login")




