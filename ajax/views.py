from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Avg, QuerySet
from django.db.models.functions import TruncDate
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404
from django.views import View

from ajax.forms import UserUpdateForm, ApproachForm, DishCountForm
from main.forms import ExerciseForm
from main.models import (Exercise,
                         Approach,
                         PowerTrainingExercise,
                         Cycling,
                         Swimming,
                         Walking,
                         Jogging,
                         PowerTraining,
                         Dish,
                         User, Meal, DishCount, Training)

SUCCESS_RESPONSE = JsonResponse({
    "status": "Success",
}, status=200)

NOT_FOUND_RESPONSE = JsonResponse({
    "status": "error",
}, status=404)

INVALID_DATA_RESPONSE = JsonResponse({
    "status": "error",
}, status=422)


class UpdatePasswordView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return JsonResponse({
                "status": "success",
            }, status=200)

        return JsonResponse({
            "status": "error",
            "errors": form.errors,
        }, status=422)


class UpdateUser(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return SUCCESS_RESPONSE

        return JsonResponse(
            {
                "status": "error",
                "errors": form.errors,
            }
        )


class AddPowerExerciseView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        exercise_id = request.POST.get("exercise_id", default=None)
        training_id = request.POST.get("training_id", default=None)

        if not exercise_id or not training_id:
            return INVALID_DATA_RESPONSE

        exercise = get_object_or_404(Exercise, pk=exercise_id)

        try:
            PowerTrainingExercise.objects.get(power_training_id=training_id,
                                              exercise_id=exercise_id)
            return INVALID_DATA_RESPONSE
        except PowerTrainingExercise.DoesNotExist:
            pass

        power_training = PowerTrainingExercise.objects.create(exercise=exercise,
                                                              power_training_id=training_id)
        return JsonResponse(
            {
                "status": "success",
                "power_training_id": power_training.id,
            }
        )


class CreateApproachView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        form = ApproachForm(request.POST, request=request)

        if form.is_valid():
            approach = form.save()
            return JsonResponse({
                "approach_id": approach.id
            }, status=200)
        else:
            return INVALID_DATA_RESPONSE


class DeletePowerExerciseView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        exercise_id = request.POST.get("exercise_id",
                                       default=None)
        training_id = request.POST.get("training_id",
                                       default=None)

        if not exercise_id or not training_id:
            return INVALID_DATA_RESPONSE

        get_object_or_404(PowerTrainingExercise,
                          pk=exercise_id,
                          power_training_id=training_id,
                          power_training__user=request.user).delete()
        return SUCCESS_RESPONSE


class DeleteApproach(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        approach = request.POST.get("approach_id", default=None)
        exercise = request.POST.get("exercise_id", default=None)

        if not approach or not exercise:
            return INVALID_DATA_RESPONSE

        get_object_or_404(Approach,
                          id=approach,
                          training__power_training__user_id=request.user.id,
                          training_id=exercise).delete()
        return SUCCESS_RESPONSE


class DeleteTrainingView(LoginRequiredMixin, View):
    @staticmethod
    def post(request) -> JsonResponse:
        training_type = request.POST.get("type",
                                         default=None)
        training_id = request.POST.get("id",
                                       default=None)
        if not training_type or not training_id:
            return INVALID_DATA_RESPONSE

        if training_type == "PW":
            get_object_or_404(PowerTraining,
                              pk=training_id,
                              user=request.user).delete()
        elif training_type == "CY":
            get_object_or_404(Cycling,
                              pk=training_id,
                              user=request.user).delete()
        elif training_type == "SW":
            get_object_or_404(Swimming,
                              pk=training_id,
                              user=request.user).delete()
        elif training_type == "WK":
            get_object_or_404(Walking,
                              pk=training_id,
                              user=request.user).delete()
        elif training_type == "JG":
            get_object_or_404(Jogging,
                              pk=training_id,
                              user=request.user).delete()
        return SUCCESS_RESPONSE


class AddDishCountView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        form = DishCountForm(request.POST, user=request.user)
        if form.is_valid():
            dish_count = form.save()
            return JsonResponse({
                "dish_count_id": dish_count.id,
            }, status=200)
        else:
            return INVALID_DATA_RESPONSE


class UpdateDishCountView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        dish_count_id = request.POST.get("dish_count", default=None)

        if not dish_count_id:
            return INVALID_DATA_RESPONSE
        dish_count = get_object_or_404(DishCount, pk=dish_count_id)
        form = DishCountForm(request.POST,
                             user=request.user,
                             instance=dish_count)
        if form.is_valid():
            form.save()
            return SUCCESS_RESPONSE
        else:
            return INVALID_DATA_RESPONSE


class DeleteDishCountView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        dish_count_id = request.POST.get("dish_count", default=None)
        if not dish_count_id:
            return INVALID_DATA_RESPONSE
        dish_count = get_object_or_404(DishCount, id=dish_count_id)
        if dish_count.meal.user != request.user:
            return INVALID_DATA_RESPONSE
        dish_count.delete()
        return SUCCESS_RESPONSE


class UpdateApproachView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        form = ApproachForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return SUCCESS_RESPONSE
        else:
            return INVALID_DATA_RESPONSE


class DeleteExerciseView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        exercise_id = request.POST.get("exercise_id", default=None)

        if not exercise_id:
            return INVALID_DATA_RESPONSE

        get_object_or_404(Exercise, id=exercise_id).delete()
        return SUCCESS_RESPONSE


class DeleteDishView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        dish_id = request.POST.get("dish_id", default=None)
        if not dish_id:
            return INVALID_DATA_RESPONSE
        get_object_or_404(Dish,
                          id=dish_id,
                          user=request.user).delete()
        return SUCCESS_RESPONSE


class DeleteMealView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        meal_id = request.POST.get("meal_id", default=None)
        if not meal_id:
            return INVALID_DATA_RESPONSE
        get_object_or_404(Meal,
                          id=meal_id,
                          user=request.user).delete()
        return SUCCESS_RESPONSE


class GetTrainingsTypeRatio(LoginRequiredMixin, View):
    @staticmethod
    def get(request: HttpRequest) -> JsonResponse:
        period = request.GET.get("period", default=None)
        if not period:
            return INVALID_DATA_RESPONSE
        period = period.lower()
        today = date.today()
        if period == "today":
            q_obj = Q(user=request.user, start__date=today)
        elif period == "this month":
            q_obj = Q(user=request.user,
                      start__month=today.month,
                      start__year=today.year)
        elif period == "this year":
            q_obj = Q(user=request.user,
                      start__year=today.year)
        else:
            return INVALID_DATA_RESPONSE

        power_trainings = PowerTraining.objects.filter(q_obj).count()
        cycling = Cycling.objects.filter(q_obj).count()
        jogging = Jogging.objects.filter(q_obj).count()
        walking = Walking.objects.filter(q_obj).count()
        swimming = Swimming.objects.filter(q_obj).count()

        response = JsonResponse(
            {
                "data": [
                    {
                        "name": "Power trainings",
                        "value": power_trainings,
                    },
                    {
                        "name": "Cycling",
                        "value": cycling,
                    },
                    {
                        "name": "Jogging",
                        "value": jogging,
                    },
                    {
                        "name": "Walking",
                        "value": walking,
                    },
                    {
                        "name": "Swimming",
                        "value": swimming,
                    },
                ]
            }, status=200)
        return response


def get_and_validate_period(request: HttpRequest) -> str | None:
    period = request.GET.get("period", default=None)
    period = period.lower()
    return period


def get_meals_by_period(period: str, user: User) -> QuerySet[Meal] | None:
    today = date.today()

    if period == "today":
        q_obj = Q(date__date=today)
    elif period == "this month":
        q_obj = Q(date__month=today.month,
                  date__year=today.year)
    elif period == "this year":
        q_obj = Q(date__year=today.year)
    else:
        return None
    return user.meals.filter(q_obj)


def get_unique_meal_dates_count(query_set: QuerySet[Meal]) -> int:
    return query_set.annotate(unique_date=TruncDate('date')).values('unique_date').distinct().count()


class GetAvgCaloriesPerDayInfo(LoginRequiredMixin, View):
    @staticmethod
    def get(request: HttpRequest) -> JsonResponse:
        if (not (period := get_and_validate_period(request)) or
                (user_meals := get_meals_by_period(period, request.user)) is None):
            return INVALID_DATA_RESPONSE

        total_calories = sum(meal.get_total_calories() for meal in user_meals)
        unique_dates_count = get_unique_meal_dates_count(user_meals)

        avg_calories_per_day = 0
        if unique_dates_count:
            avg_calories_per_day = total_calories / unique_dates_count

        response = JsonResponse({
            "data": avg_calories_per_day,
        }, status=200)
        return response


class GetAvgProteinPerDayView(LoginRequiredMixin, View):
    @staticmethod
    def get(request: HttpRequest) -> JsonResponse:
        if (not (period := get_and_validate_period(request)) or
                (user_meals := get_meals_by_period(period, request.user)) is None):
            return INVALID_DATA_RESPONSE

        total_protein = sum(meal.get_total_protein() for meal in user_meals)
        unique_dates_count = get_unique_meal_dates_count(user_meals)

        avg_protein_per_day = 0
        if unique_dates_count:
            avg_protein_per_day = total_protein / unique_dates_count

        response = JsonResponse({
            "data": avg_protein_per_day,
        }, status=200)
        return response


class GetAvgCarbohydratesPerDayView(LoginRequiredMixin, View):
    @staticmethod
    def get(request: HttpRequest) -> JsonResponse:
        if (not (period := get_and_validate_period(request)) or
                (user_meals := get_meals_by_period(period, request.user)) is None):
            return INVALID_DATA_RESPONSE

        total_protein = sum(meal.get_total_carbohydrates() for meal in user_meals)
        unique_dates_count = get_unique_meal_dates_count(user_meals)

        avg_carbohydrates_per_day = 0
        if unique_dates_count:
            avg_carbohydrates_per_day = total_protein / unique_dates_count

        response = JsonResponse({
            "data": avg_carbohydrates_per_day,
        }, status=200)

        return response


class GetAvgFatsPerDayView(LoginRequiredMixin, View):
    @staticmethod
    def get(request: HttpRequest) -> JsonResponse:
        if (not (period := get_and_validate_period(request)) or
                (user_meals := get_meals_by_period(period, request.user)) is None):
            return INVALID_DATA_RESPONSE

        total_fats = sum(meal.get_total_fats() for meal in user_meals)
        unique_dates_count = get_unique_meal_dates_count(user_meals)

        avg_fats_per_day = 0
        if unique_dates_count:
            avg_fats_per_day = total_fats / unique_dates_count

        response = JsonResponse({
            "data": avg_fats_per_day,
        }, status=200)

        return response

