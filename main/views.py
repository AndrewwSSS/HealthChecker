from datetime import datetime

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
)
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import NoReverseMatch
from django.views import generic

from main.forms import (
    CyclingForm,
    DateSearchForm,
    DishForm,
    ExerciseForm,
    JoggingForm,
    MealForm,
    NameSearchForm,
    PowerTrainingForm,
    SwimmingForm,
    UserCreateForm,
    UserLoginForm,
    WalkingForm,
)
from main.models import (
    Cycling,
    Dish,
    Exercise,
    Jogging,
    Meal,
    PowerTraining,
    Swimming,
    User,
    Walking,
)


class BaseListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = datetime.today()
        return context


class DateSearchListViewMixin(BaseListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = self.request.GET.get("start_date", None)
        end_date = self.request.GET.get("end_date", None)
        sort = self.request.GET.get("sort", None)

        context["search_form"] = DateSearchForm(
            initial={
                "start_date": start_date,
                "end_date": end_date,
                "sort": sort
            }
        )
        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)
        form = DateSearchForm(self.request.GET)

        if not form.is_valid() or not queryset.count():
            return queryset

        start_date = form.cleaned_data.get("start_date", None)
        end_date = form.cleaned_data.get("end_date", None)

        if start_date:
            if end_date:
                queryset = queryset.filter(
                    date__date__gte=start_date, date__date__lte=end_date
                )
            else:
                queryset = queryset.filter(date__date__gte=start_date)
        else:
            if end_date:
                queryset = queryset.filter(date__date__lte=end_date)

        sort_type = form.cleaned_data.get("sort", None)
        if sort_type == "DESC":
            queryset = queryset.order_by("-date")
        elif sort_type == "ASC":
            queryset = queryset.order_by("date")
        return queryset


class DateSearchTrainingListView(DateSearchListViewMixin):
    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)
        form = DateSearchForm(self.request.GET)

        if not form.is_valid() or not queryset.count():
            print(form.errors)
            return queryset

        start_date = form.cleaned_data.get("start_date", None)
        end_date = form.cleaned_data.get("end_date", None)
        if start_date:
            if end_date:
                queryset = queryset.filter(
                    start__date__gte=start_date, start__date__lte=end_date
                )
            else:
                queryset = queryset.filter(start__date__gte=start_date)
        else:
            if end_date:
                queryset = queryset.filter(start__date__lte=end_date)

        sort_type = form.cleaned_data.get("sort", None)
        if sort_type == "DESC":
            queryset = queryset.order_by("-start")
        elif sort_type == "ASC":
            queryset = queryset.order_by("start")

        return queryset


class NameSearchListView(DateSearchListViewMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = self.request.GET.get("name", None)
        sort = self.request.GET.get("sort", None)

        context["search_form"] = DateSearchForm(
            initial={
                "name": date,
                "sort": sort
            }
        )
        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)
        form = NameSearchForm(self.request.GET)
        if not form.is_valid() or not queryset.count():
            return queryset

        if name := form.cleaned_data.get("name", None):
            queryset = queryset.filter(name__icontains=name)

        sort_type = form.cleaned_data.get("sort", None)
        if sort_type == "DESC":
            queryset = queryset.order_by("-name")
        elif sort_type == "ASC":
            queryset = queryset.order_by("name")
        return queryset


class CreateElementWithUserFieldView(LoginRequiredMixin, generic.CreateView):
    def form_valid(self, form):
        element = form.save(commit=False)
        element.user = self.request.user
        element.save()
        try:
            return redirect(self.success_url)
        except NoReverseMatch:
            return redirect(self.success_url, pk=element.pk)


class UpdateElementWithUserFieldView(LoginRequiredMixin, generic.UpdateView):
    def form_valid(self, form):
        element = form.save(commit=False)
        if element.user != self.request.user:
            return render(self.request, "404.html")
        element.save()
        return redirect(self.success_url)

    def get(self, request: HttpRequest, *args, **kwargs):
        pk = kwargs.get("pk", None)
        get_object_or_404(self.model, pk=pk, user=self.request.user)
        return super().get(request, *args, **kwargs)


class LoginUserView(LoginView):
    form_class = UserLoginForm

    def form_valid(self, form):
        if not form.cleaned_data.get("remember_me", None):
            self.request.session.set_expiry(0)
            self.request.session.modified = True
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


class ExercisesListView(NameSearchListView):
    model = Exercise
    template_name = "main/exercise/exercises-list.html"


class ExerciseUpdateView(UpdateElementWithUserFieldView):
    model = Exercise
    template_name = "main/exercise/exercise-form.html"
    success_url = "main:exercises-list"
    form_class = ExerciseForm


class ExerciseCreateView(CreateElementWithUserFieldView):
    model = Exercise
    template_name = "main/exercise/exercise-form.html"
    form_class = ExerciseForm
    success_url = "main:exercises-list"


class DishListView(NameSearchListView):
    model = Dish
    template_name = "main/dish/dish-list.html"


class CreateDishView(CreateElementWithUserFieldView):
    model = Dish
    form_class = DishForm
    template_name = "main/dish/create-dish.html"
    success_url = "main:dish-list"


class UpdateDishView(UpdateElementWithUserFieldView):
    model = Dish
    form_class = DishForm
    template_name = "main/dish/update-dish.html"
    success_url = "main:dish-list"


# Trainings list view
class PowerTrainingsListView(DateSearchTrainingListView):
    model = PowerTraining
    template_name = "main/trainings/power-training/power-trainings-list.html"


class CyclingTrainingListView(DateSearchTrainingListView):
    model = Cycling
    template_name = ("main/trainings/cycling_training/"
                     "cycling-training-list.html")


class SwimmingTrainingListView(DateSearchTrainingListView):
    model = Swimming
    template_name = "main/trainings/swimming_training/swimming-list.html"


class JoggingTrainingListView(DateSearchTrainingListView):
    model = Jogging
    template_name = "main/trainings/jogging_trainings/jogging-list.html"


class WalkingTrainingListView(DateSearchTrainingListView):
    model = Walking
    template_name = "main/trainings/walk/walking-list.html"


# Create training views
class CreatePowerTrainingView(CreateElementWithUserFieldView):
    template_name = "main/trainings/power-training/create-power-training.html"
    model = PowerTraining
    form_class = PowerTrainingForm
    success_url = "main:update-power-training"


class CreateSwimmingView(CreateElementWithUserFieldView):
    model = Swimming
    form_class = SwimmingForm
    template_name = "base_distance_average_speed_form.html"
    success_url = "main:swimming-training-list"


class CreateJoggingView(CreateElementWithUserFieldView):
    model = Jogging
    form_class = JoggingForm
    template_name = "base_distance_average_speed_form.html"
    success_url = "main:jogging-training-list"


class CreateWalkingView(CreateElementWithUserFieldView):
    model = Walking
    form_class = WalkingForm
    template_name = "base_distance_average_speed_form.html"
    success_url = "main:walking-training-list"


class CreateCyclingTrainingView(CreateElementWithUserFieldView):
    model = Cycling
    form_class = CyclingForm
    template_name = ("main/trainings/cycling_training/"
                     "cycling-training-form.html")
    success_url = "main:cycling-training-list"


# update training views
class UpdatePowerTrainingView(UpdateElementWithUserFieldView):
    model = PowerTraining
    template_name = "main/trainings/power-training/update-power-training.html"
    form_class = PowerTrainingForm
    success_url = "main:power-trainings-list"

    def get_context_data(self, **kwargs):
        context = (super(UpdatePowerTrainingView, self)
                   .get_context_data(**kwargs))
        context["exercises"] = (Exercise.objects
                                .filter(user=self.request.user))
        return context


class UpdateSwimmingView(UpdateElementWithUserFieldView):
    fields = SwimmingForm.Meta.fields
    model = Swimming
    class_form = SwimmingForm
    template_name = "base_distance_average_speed_form.html"
    success_url = "main:swimming-training-list"


class UpdateJoggingView(UpdateElementWithUserFieldView):
    fields = JoggingForm.Meta.fields
    model = Jogging
    class_form = JoggingForm
    template_name = "base_distance_average_speed_form.html"
    success_url = "main:swimming-training-list"


class UpdateWalkingView(UpdateElementWithUserFieldView):
    fields = WalkingForm.Meta.fields
    model = Walking
    class_form = WalkingForm
    template_name = "base_distance_average_speed_form.html"
    success_url = "main:walking-training-list"


class UpdateCyclingTrainingView(UpdateElementWithUserFieldView):
    fields = CyclingForm.Meta.fields
    model = Cycling
    class_form = CyclingForm
    template_name = ("main/trainings/cycling_training/"
                     "cycling-training-form.html")
    success_url = "main:cycling-training-list"


# ------


class MealListView(DateSearchListViewMixin):
    model = Meal
    template_name = "main/meal/meal-list.html"


class CreateMealView(CreateElementWithUserFieldView):
    model = Meal
    form_class = MealForm
    template_name = "main/meal/create-meal.html"
    success_url = "main:update-meal"

    def get_context_data(self, **kwargs):
        context = super(CreateMealView, self).get_context_data(**kwargs)
        context["default_date"] = datetime.now()
        return context


class UpdateMealView(UpdateElementWithUserFieldView):
    model = Meal
    form_class = MealForm
    template_name = "main/meal/update-meal.html"
    success_url = "main:meal-list"
