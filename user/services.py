from abc import ABC
from enum import Enum
from typing import Type

from django.db.models import Q, QuerySet
from django.db.models.functions import TruncDate
from django.utils import timezone

from main.models import (
    Cycling,
    DistanceAverageSpeedMixin,
    Jogging,
    Meal,
    PowerTraining,
    Swimming,
    User,
    Walking,
)
from main.models import Training


class PERIOD(Enum):
    TODAY = "today"
    THIS_MONTH = "this month"
    THIS_YEAR = "this year"


class UserBasedStatisticService(ABC):
    date_field = "date"

    def __init__(
        self, user: User,
    ) -> None:
        self.user = user

    def get_filter_by_period(self, period: str) -> Q:
        """
        Generates a Q object for filtering based on the period and date field.
        :param period: The period to filter by (e.g., 'today', 'this month', 'this year')
        :param date_field: The field used for date comparison (e.g., 'date' or 'start')
        :return: Q object for filtering
        """
        today = timezone.now().today()
        if period == PERIOD.TODAY.value:
            return Q(**{f"{self.date_field}__date": today})
        elif period == PERIOD.THIS_MONTH.value:
            return Q(
                **{
                    f"{self.date_field}__month": today.month,
                    f"{self.date_field}__year": today.year
                }
            )
        elif period == PERIOD.THIS_YEAR.value:
            return Q(**{f"{self.date_field}__year": today.year})

    @staticmethod
    def clean_period(period: str) -> str:
        if not isinstance(period, str):
            raise TypeError("period must be str")

        period = period.lower()
        correct_periods = [p.value for p in PERIOD]
        if period not in correct_periods:
            raise ValueError("period must be one of {}".format(correct_periods))
        return period


class MealStatisticService(UserBasedStatisticService):
    def get_user_meals(
        self,
        period: str
    ) -> QuerySet[Meal]:

        return self.user.meals.filter(
            self.get_filter_by_period(period)
        )

    @staticmethod
    def get_unique_meal_dates_count(query_set: QuerySet[Meal]) -> int:
        return (
            query_set.annotate(unique_date=TruncDate("date"))
            .values("unique_date")
            .distinct()
            .count()
        )

    def get_avg_macronutrient(self, period: str, calc_total: callable) -> float:
        period = self.clean_period(period)
        meals = self.get_user_meals(period)

        total_weight = calc_total(meals)
        unique_dates_count = self.get_unique_meal_dates_count(meals)

        avg_macronutrient = 0
        if unique_dates_count:
            avg_macronutrient = total_weight / unique_dates_count
        return round(avg_macronutrient, 1)

    def get_avg_carbohydrates(self, period: str) -> float:
        return self.get_avg_macronutrient(
            period, lambda meals: sum(
                meal.get_total_carbohydrates()
                for meal in meals
            )
        )

    def get_avg_protein(self, period: str) -> float:
        return self.get_avg_macronutrient(
            period,
            lambda meals: sum(meal.get_total_protein() for meal in meals)
        )

    def get_avg_fats(self, period: str) -> float:
        return self.get_avg_macronutrient(
            period,
            lambda meals: sum(meal.get_total_fats() for meal in meals)
        )

    def get_avg_calories(self, period: str) -> float:
        return self.get_avg_macronutrient(
            period,
            lambda meals: sum(meal.get_total_calories() for meal in meals)
        )

    def get_pfc_ratio(self, period: str) -> list[dict]:
        period = self.clean_period(period)
        meals = self.get_user_meals(period)

        protein = sum(
            meal.get_total_protein() for meal in meals
        )
        carbohydrates = sum(
            meal.get_total_carbohydrates() for meal in meals
        )
        fats = sum(
            meal.get_total_fats() for meal in meals
        )
        return [
            {
                "name": "protein",
                "value": protein,
            },
            {
                "name": "carbohydrates",
                "value": carbohydrates,
            },
            {
                "name": "fats",
                "value": fats
            },
        ]


class TrainingStatisticService(UserBasedStatisticService):
    date_field = "start"

    def get_trainings(
        self, training_type: Type[Training], period: str = None
    ) -> QuerySet[type]:
        queryset = training_type.objects.filter(user=self.user)

        return queryset.filter(
            self.get_filter_by_period(period)
        )

    def get_total_km(
        self, period: str, training_type: Type[DistanceAverageSpeedMixin]
    ) -> float:
        if not issubclass(training_type, DistanceAverageSpeedMixin):
            raise TypeError("training must be DistanceAverageSpeedMixin")

        trainings = self.get_trainings(
            training_type,
            self.clean_period(period),
        )
        return sum(training.distance for training in trainings)

    def get_trainings_type_ratio(self, period: str) -> list[dict]:
        period = self.clean_period(period)
        power_trainings = self.get_trainings(PowerTraining, period).count()
        cycling = self.get_trainings(Cycling, period).count()
        jogging = self.get_trainings(Jogging, period).count()
        walking = self.get_trainings(Walking, period).count()
        swimming = self.get_trainings(Swimming, period).count()

        return [
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
