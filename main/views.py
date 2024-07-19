from datetime import datetime
from typing import Any

from django.contrib.auth import logout, login as auth_login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet, Q
from django.http import (HttpResponse,
                         HttpRequest,
                         HttpResponseRedirect,
                         Http404)
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic

from main.forms import (UserCreateForm,
                        PowerTrainingForm,
                        ExerciseForm,
                        CyclingForm,
                        DishForm,
                        SwimmingForm,
                        JoggingForm,
                        WalkingForm,
                        MealForm,
                        DateSearchForm,
                        NameSearchForm,
                        UserLoginForm)
from main.models import (User,
                         PowerTraining,
                         Exercise,
                         Cycling,
                         Dish,
                         Swimming,
                         Jogging,
                         Walking,
                         Meal)


class LoginUserView(LoginView):
    form_class = UserLoginForm

    def form_valid(self, form):
        if not self.request.POST.get('remember_me', None):
            self.request.session.set_expiry(0)
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect("/accounts/login")


class HomePageView(LoginRequiredMixin, generic.TemplateView):
    template_name = "base.html"
    login_url = "accounts/login"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context


class UserProfileView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = "main/user/user-detail.html"

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


class ExercisesListView(LoginRequiredMixin, generic.ListView):
    model = Exercise
    template_name = "main/exercise/exercises-list.html"
    paginate_by = 30

    def get_queryset(self):
        queryset = Exercise.objects.all()
        return get_queryset_for_name_search_form(queryset, self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ExercisesListView, self).get_context_data(**kwargs)
        return update_context_for_name_search_form(context, self.request)


class ExerciseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Exercise
    template_name = "main/exercise/exercise-form.html"
    success_url = "/exercises/"
    form_class = ExerciseForm

    def post(self, request, *args, **kwargs):
        exercise = get_object_or_404(Exercise, pk=kwargs.get("pk", -1))
        form = ExerciseForm(request.POST, user=request.user, instance=exercise)
        if form.is_valid():
            form.save()
            return redirect("main:exercises-list")
        else:
            return render(request, self.template_name, {"object": form.instance})


class ExerciseCreateView(LoginRequiredMixin, generic.CreateView):
    model = Exercise
    template_name = "main/exercise/exercise-form.html"
    form_class = ExerciseForm
    success_url = "/exercises/"

    def post(self, request, *args, **kwargs):
        form = ExerciseForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("main:exercises-list")
        else:
            return render(request, self.template_name, context=self.get_context_data())


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    template_name = "main/dish/dish-list.html"
    paginate_by = 30

    def get_queryset(self):
        queryset = Dish.objects.filter(user=self.request.user)
        return get_queryset_for_name_search_form(queryset, self.request)

    def get_context_data(self, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        return update_context_for_name_search_form(context, self.request)


class CreateDishView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    template_name = "main/dish/create-dish.html"
    success_url = "/dishes/"


class UpdateDishView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    template_name = "main/dish/update-dish.html"
    success_url = "/dishes/"


# Trainings list view
class PowerTrainingsListView(LoginRequiredMixin, generic.ListView):
    model = PowerTraining
    template_name = "main/trainings/power-training/power-trainings-list.html"

    def get_queryset(self):
        queryset = PowerTraining.objects.filter(user=self.request.user)
        return get_queryset_for_date_search_form(queryset, self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PowerTrainingsListView, self).get_context_data(**kwargs)
        return update_context_for_date_search_form(context, self.request)


class CyclingTrainingListView(LoginRequiredMixin, generic.ListView):
    model = Cycling
    template_name = "main/trainings/cycling_training/cycling-training-list.html"

    def get_queryset(self):
        queryset = Cycling.objects.filter(user=self.request.user)
        return get_queryset_for_date_search_form(queryset, self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CyclingTrainingListView, self).get_context_data(**kwargs)
        return update_context_for_date_search_form(context, self.request)


class SwimmingTrainingListView(LoginRequiredMixin, generic.ListView):
    model = Swimming
    template_name = "main/trainings/swimming_training/swimming-list.html"

    def get_queryset(self):
        queryset = Swimming.objects.filter(user=self.request.user)
        return get_queryset_for_date_search_form(queryset, self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SwimmingTrainingListView, self).get_context_data(**kwargs)
        return update_context_for_date_search_form(context, self.request)


class JoggingTrainingListView(LoginRequiredMixin, generic.ListView):
    model = Jogging
    template_name = "main/trainings/jogging_trainings/jogging-list.html"

    def get_queryset(self):
        queryset = Jogging.objects.filter(user=self.request.user)
        return get_queryset_for_date_search_form(queryset, self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(JoggingTrainingListView, self).get_context_data(**kwargs)
        return update_context_for_date_search_form(context, self.request)


class WalkingTrainingListView(LoginRequiredMixin, generic.ListView):
    model = Walking
    template_name = "main/trainings/walk/walking-list.html"

    def get_queryset(self):
        queryset = Walking.objects.filter(user=self.request.user)
        return get_queryset_for_date_search_form(queryset, self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WalkingTrainingListView, self).get_context_data(**kwargs)
        return update_context_for_date_search_form(context, self.request)


# Create training views
class CreatePowerTrainingView(LoginRequiredMixin, generic.CreateView):
    template_name = "main/trainings/power-training/create-power-training.html"
    model = PowerTraining
    form_class = PowerTrainingForm

    def form_valid(self, form):
        training = form.save()
        return redirect("main:update-power-training", pk=training.pk)


class CreateSwimmingView(LoginRequiredMixin, generic.CreateView):
    model = Swimming
    form_class = SwimmingForm
    template_name = "base_distance_average_speed_form.html"
    success_url = "/swimming-trainings/"


class CreateJoggingView(LoginRequiredMixin, generic.CreateView):
    model = Jogging
    form_class = JoggingForm
    template_name = "base_distance_average_speed_form.html"
    success_url = "/jogging-trainings/"


class CreateWalkingView(LoginRequiredMixin, generic.CreateView):
    model = Walking
    form_class = WalkingForm
    template_name = "base_distance_average_speed_form.html"
    success_url = "/walking-trainings/"


class CreateCyclingTrainingView(LoginRequiredMixin, generic.CreateView):
    model = Cycling
    form_class = CyclingForm
    template_name = "main/trainings/cycling_training/cycling-training-form.html"
    success_url = "/cycling-trainings/"


# update training views
class UpdatePowerTrainingView(LoginRequiredMixin, generic.UpdateView):
    model = PowerTraining
    template_name = "main/trainings/power-training/update-power-training.html"
    form_class = PowerTrainingForm
    success_url = "/power-trainings/"

    def get_context_data(self, **kwargs):
        context = super(UpdatePowerTrainingView, self).get_context_data(**kwargs)
        context["exercises"] = Exercise.objects.all()
        return context


class UpdateSwimmingView(LoginRequiredMixin, generic.UpdateView):
    fields = "__all__"
    model = Swimming
    class_form = SwimmingForm
    template_name = "base_distance_average_speed_form.html"
    success_url = "/swimming-trainings/"


class UpdateJoggingView(LoginRequiredMixin, generic.UpdateView):
    fields = "__all__"
    model = Jogging
    class_form = JoggingForm
    template_name = "base_distance_average_speed_form.html"
    success_url = "/jogging-trainings/"


class UpdateWalkingView(LoginRequiredMixin, generic.UpdateView):
    fields = "__all__"
    model = Walking
    class_form = WalkingForm
    template_name = "base_distance_average_speed_form.html"
    success_url = "/walking-trainings/"


class UpdateCyclingTrainingView(LoginRequiredMixin, generic.UpdateView):
    fields = "__all__"
    model = Cycling
    class_form = CyclingForm
    template_name = "main/trainings/cycling_training/cycling-training-form.html"
    success_url = "/cycling-trainings/"
# ------


class MealListView(LoginRequiredMixin, generic.ListView):
    model = Meal
    template_name = "main/meal/meal-list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MealListView, self).get_context_data(**kwargs)
        context["today"] = datetime.today()
        return update_context_for_date_search_form(context, self.request)

    def get_queryset(self):
        queryset = Meal.objects.filter(user=self.request.user)
        date = self.request.GET.get("date", "")
        if date:
            try:
                date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError as e:
                raise Http404("Invalid date")

        sort = self.request.GET.get("sort")

        form = DateSearchForm(self.request.GET)
        if not form.is_valid() or not queryset.count():
            return queryset

        if date:
            base_queryset = queryset.filter(date__day=date.day,
                                            date__month=date.month,
                                            date__year=date.year)
        if sort == "DESC":
            base_queryset = queryset.order_by("-date")
        else:
            base_queryset = queryset.order_by("date")

        return base_queryset


class CreateMealView(LoginRequiredMixin, generic.CreateView):
    model = Meal
    form_class = MealForm
    template_name = "main/meal/create-meal.html"

    def get_context_data(self, **kwargs):
        context = super(CreateMealView, self).get_context_data(**kwargs)
        context["default_date"] = datetime.now()
        return context

    def form_valid(self, form):
        meal = form.save()
        return redirect("main:update-meal", pk=meal.pk)


class UpdateMealView(LoginRequiredMixin, generic.UpdateView):
    model = Meal
    form_class = MealForm
    template_name = "main/meal/update-meal.html"
    success_url = "/meals/"


def update_context_for_name_search_form(base_context: dict[str, Any],
                                        request: HttpRequest) -> dict[str, Any]:
    name = request.GET.get("name", "")
    base_context["search_form"] = NameSearchForm(
        initial={
            "name": name
        }
    )
    return update_contex_for_sort(base_context, request)


def update_contex_for_sort(base_context: dict[str, Any], request: HttpRequest) -> dict[str, Any]:
    sort = request.GET.get("sort", None)
    base_context["search_form"] = DateSearchForm(
        initial={
            "sort": sort
        }
    )
    return base_context


def update_context_for_date_search_form(base_context: dict[str, Any],
                                        request: HttpRequest) -> dict[str, Any]:
    date = request.GET.get("date", None)

    base_context["search_form"] = DateSearchForm(
        initial={
            "date": date,
        }
    )
    return update_contex_for_sort(base_context, request)


def get_queryset_for_name_search_form(base_queryset: QuerySet,
                                      request: HttpRequest) -> QuerySet:
    form = NameSearchForm(request.GET)
    if not form.is_valid() or not base_queryset.count():
        return base_queryset

    if name := form.cleaned_data.get("name", None):
        base_queryset = base_queryset.filter(name__icontains=name)

    if form.cleaned_data.get("sort", None) == "DESC":
        base_queryset = base_queryset.order_by("-name")
    else:
        base_queryset = base_queryset.order_by("name")

    return base_queryset


def get_queryset_for_date_search_form(base_queryset: QuerySet,
                                      request: HttpRequest) -> QuerySet:
    form = DateSearchForm(request.GET)
    if not form.is_valid() or not base_queryset.count():
        return base_queryset

    if date := form.cleaned_data["date"]:
        base_queryset = base_queryset.filter(start__day=date.day,
                                             start__month=date.month,
                                             start__year=date.year)
    if form.cleaned_data["sort"] == "DESC":
        base_queryset = base_queryset.order_by("-start")
    else:
        base_queryset = base_queryset.order_by("start")

    return base_queryset
