from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models import QuerySet
from django.db.models.functions import TruncDate
from django.http import HttpRequest
from django.http import JsonResponse
from django.views import View

from ajax.views import INVALID_DATA_RESPONSE
from main.models import Cycling
from main.models import Jogging
from main.models import Meal
from main.models import PowerTraining
from main.models import Swimming
from main.models import Training
from main.models import User
from main.models import Walking


class GetTrainingsTypeRatioView(LoginRequiredMixin, View):
    @staticmethod
    def get(request: HttpRequest) -> JsonResponse:
        if not (period := get_and_validate_period(request)):
            return INVALID_DATA_RESPONSE

        today = date.today()
        if period == "today":
            q_obj = Q(user=request.user, start__date=today)
        elif period == "this month":
            q_obj = Q(
                user=request.user,
                start__month=today.month,
                start__year=today.year
            )
        elif period == "this year":
            q_obj = Q(user=request.user, start__year=today.year)
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
            },
            status=200,
        )
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
        q_obj = Q(date__month=today.month, date__year=today.year)
    elif period == "this year":
        q_obj = Q(date__year=today.year)
    else:
        return None
    return user.meals.filter(q_obj)


def get_trainings_by_period_and_user(
    period: str, user: User, training_type: type[Training]
) -> QuerySet[Training] | None:
    today = date.today()
    if period == "today":
        q_obj = Q(start__date=today)
    elif period == "this month":
        q_obj = Q(start__month=today.month, start__year=today.year)
    elif period == "this year":
        q_obj = Q(start__year=today.year)
    else:
        return None
    return training_type.objects.filter(q_obj, user=user)


def get_unique_meal_dates_count(query_set: QuerySet[Meal]) -> int:
    return (
        query_set.annotate(unique_date=TruncDate("date"))
        .values("unique_date")
        .distinct()
        .count()
    )


class GetAvgCaloriesPerDayInfo(LoginRequiredMixin, View):
    @staticmethod
    def get(request: HttpRequest) -> JsonResponse:
        if (
            not (period := get_and_validate_period(request))
            or not (user_meals := get_meals_by_period(period, request.user))
        ):
            return INVALID_DATA_RESPONSE

        total_calories = sum(meal.get_total_calories() for meal in user_meals)
        unique_dates_count = get_unique_meal_dates_count(user_meals)

        avg_calories_per_day = 0
        if unique_dates_count:
            avg_calories_per_day = total_calories / unique_dates_count

        response = JsonResponse(
            {
                "data": round(avg_calories_per_day, 1),
            },
            status=200,
        )
        return response


class GetAvgProteinPerDayView(LoginRequiredMixin, View):
    @staticmethod
    def get(request: HttpRequest) -> JsonResponse:
        if (
            not (period := get_and_validate_period(request))
            or not (user_meals := get_meals_by_period(period, request.user))
        ):
            return INVALID_DATA_RESPONSE

        total_protein = sum(meal.get_total_protein() for meal in user_meals)
        unique_dates_count = get_unique_meal_dates_count(user_meals)

        avg_protein_per_day = 0
        if unique_dates_count:
            avg_protein_per_day = total_protein / unique_dates_count

        response = JsonResponse(
            {
                "data": round(avg_protein_per_day, 1),
            },
            status=200,
        )
        return response


class GetAvgCarbohydratesPerDayView(LoginRequiredMixin, View):
    @staticmethod
    def get(request: HttpRequest) -> JsonResponse:
        if (
            not (period := get_and_validate_period(request))
            or not (user_meals := get_meals_by_period(period, request.user))
        ):
            return INVALID_DATA_RESPONSE

        total_protein = sum(
            meal.get_total_carbohydrates() for meal in user_meals
        )
        unique_dates_count = get_unique_meal_dates_count(user_meals)

        avg_carbohydrates_per_day = 0
        if unique_dates_count:
            avg_carbohydrates_per_day = total_protein / unique_dates_count

        response = JsonResponse(
            {
                "data": round(avg_carbohydrates_per_day, 1),
            },
            status=200,
        )

        return response


class GetAvgFatsPerDayView(LoginRequiredMixin, View):
    @staticmethod
    def get(request: HttpRequest) -> JsonResponse:
        if (
            not (period := get_and_validate_period(request))
            or not (user_meals := get_meals_by_period(period, request.user))
        ):
            return INVALID_DATA_RESPONSE

        total_fats = sum(meal.get_total_fats() for meal in user_meals)
        unique_dates_count = get_unique_meal_dates_count(user_meals)

        avg_fats_per_day = 0
        if unique_dates_count:
            avg_fats_per_day = total_fats / unique_dates_count

        response = JsonResponse(
            {
                "data": round(avg_fats_per_day, 1),
            },
            status=200,
        )

        return response


class GetTotalKmTraining(LoginRequiredMixin, View):
    training_type: type[Training]

    def get(self, request: HttpRequest) -> JsonResponse:
        if not (period := get_and_validate_period(request)):
            return INVALID_DATA_RESPONSE
        trainings = get_trainings_by_period_and_user(
            period, request.user, self.training_type
        )
        total_kilometers = sum(training.distance for training in trainings)

        response = JsonResponse(
            {
                "data": total_kilometers,
            },
            status=200,
        )
        return response


class GetTotalKMbyCycling(GetTotalKmTraining):
    training_type = Cycling


class GetTotalKMbyJogging(GetTotalKmTraining):
    training_type = Jogging


class GetTotalKMbyWalking(GetTotalKmTraining):
    training_type = Walking


class GetTotalKMbySwimming(GetTotalKmTraining):
    training_type = Swimming


class GetPFCratio(LoginRequiredMixin, View):
    @staticmethod
    def get(request: HttpRequest) -> JsonResponse:
        if not (period := get_and_validate_period(request)) or not (
            meals := get_meals_by_period(period, request.user)
        ):
            return INVALID_DATA_RESPONSE

        protein_weight = sum(
            meal.get_total_protein() for meal in meals
        )
        carbohydrates_weight = sum(
            meal.get_total_carbohydrates() for meal in meals
        )
        fats_weight = sum(
            meal.get_total_fats() for meal in meals
        )

        response = JsonResponse(
            {
                "data": [
                    {
                        "name": "protein",
                        "value": int(protein_weight),
                    },
                    {
                        "name": "carbohydrates",
                        "value": int(carbohydrates_weight)
                    },
                    {
                        "name": "fats",
                        "value": int(fats_weight)
                    },
                ]
            },
            status=200,
        )
        return response