from typing import Type

from django.db.models import (
    Q,
    QuerySet,
    Sum,
)
from django.db.models.functions import TruncDate
from django.utils import timezone

from main.models import (
    Cycling,
    DistanceAverageSpeedMixin,
    Jogging,
    Meal,
    PowerTraining,
    Swimming,
    Training,
    User,
    Walking,
)

FILTER_PERIODS = ("today", "this month", "this year")
DISTANCE_TRAINING_MODELS = (Cycling, Walking, Jogging, Swimming)


class UserStatisticService:
    def __init__(self, user: User) -> None:
        self.user = user

    def get_user_meals(
            self,
            period: str
    ) -> QuerySet[Meal] | None:
        today = timezone.now().today()

        if period == "today":
            q_obj = Q(date__date=today)
        elif period == "this month":
            q_obj = Q(date__month=today.month, date__year=today.year)
        elif period == "this year":
            q_obj = Q(date__year=today.year)
        else:
            return None
        return self.user.meals.filter(q_obj)

    @staticmethod
    def get_unique_meal_dates_count(query_set: QuerySet[Meal]) -> int:
        return (
            query_set.annotate(unique_date=TruncDate("date"))
            .values("unique_date")
            .distinct()
            .count()
        )

    @staticmethod
    def clean_period(period: str) -> str:
        if not isinstance(period, str):
            raise TypeError("period must be str")
        period = period.lower()
        if period not in FILTER_PERIODS:
            raise ValueError("period must be one of {}".format(FILTER_PERIODS))
        return period

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
            period, lambda meals: sum(meal.get_total_carbohydrates()
                                      for meal in meals)
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

    def get_trainings(self, training_type: type, period: str = None) -> QuerySet[type]:
        return self.get_trainings_by_period(period, self.user, training_type)

    @staticmethod
    def get_trainings_by_period(period: str, user: User, training_type: type) -> QuerySet[type]:
        today = timezone.now().today()
        queryset = training_type.objects.filter(user=user)
        if period == "today":
            q_obj = Q(start__date=today)
        elif period == "this month":
            q_obj = Q(start__month=today.month, start__year=today.year)
        elif period == "this year":
            q_obj = Q(start__year=today.year)
        else:
            return queryset
        return queryset.filter(q_obj)



    def get_total_km(self, period: str, training_type: type) -> float:
        if not issubclass(training_type, DistanceAverageSpeedMixin):
            raise TypeError("training must be DistanceAverageSpeedMixin")

        trainings = self.get_trainings(
            training_type,
            self.clean_period(period),
        )
        return sum(training.distance for training in trainings)

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
